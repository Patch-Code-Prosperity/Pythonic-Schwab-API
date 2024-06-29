"""
This module provides the APIClient class for interacting with the Schwab API.
It handles authentication, token management, and making authenticated requests.
"""

import random
import re
from time import sleep
import webbrowser
import base64
import json
from datetime import datetime, timedelta
import logging
import requests

from pythonic_schwab_api.config import APIConfig
from pythonic_schwab_api.color_print import ColorPrint


class APIClient:
    """
    APIClient handles the authentication and interaction with the Schwab API.

    Attributes:
        initials (str): User initials for identifying token files.
        account_numbers (list): List of account numbers associated with the user.
        config (APIConfig): Configuration object for API settings.
        session (requests.Session): HTTP session for making requests.
        token_info (dict): Information about the current authentication token.
    """

    def __init__(self, initials):
        """
        Initialize the APIClient with user initials.

        Args:
            initials (str): User initials for identifying token files.
        """
        self.initials = initials
        self.account_numbers = None
        self.config = APIConfig(self.initials)
        self.session = requests.Session()
        self.setup_logging()
        self.token_info = self.load_token()

        # Validate and refresh token or reauthorize if necessary
        if not self.token_info or not self.ensure_valid_token():
            self.manual_authorization_flow()

    def setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(**self.config.logging_config)
        self.logger = logging.getLogger(__name__)

    def ensure_valid_token(self):
        """Ensure the token is valid, refresh if possible, otherwise prompt for reauthorization."""
        if self.token_info:
            if self.validate_token():
                self.logger.info("Token loaded and valid.")
                return True
            if 'refresh_token' in self.token_info:
                self.logger.info("Access token expired. Attempting to refresh.")
                if self.refresh_access_token():
                    return True
        self.logger.warning("Token invalid and could not be refreshed.")
        return False

    def manual_authorization_flow(self):
        """Handle the manual steps required to get the authorization code from the user."""
        self.logger.info("Starting manual authorization flow.")
        auth_url = f"{self.config.api_base_url}/v1/oauth/authorize?client_id={self.config.app_key}&redirect_uri={self.config.callback_url}&response_type=code"
        webbrowser.open(auth_url)
        self.logger.info("Please authorize the application by visiting: %s", auth_url)
        response_url = ColorPrint.input(
            "After authorizing, wait for it to load (<1min) and paste the WHOLE url here: ")
        authorization_code = f"{response_url[response_url.index('code=') + 5:response_url.index('%40')]}@"
        self.exchange_authorization_code_for_tokens(authorization_code)

    def exchange_authorization_code_for_tokens(self, code):
        """Exchange the authorization code for access and refresh tokens."""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config.callback_url
        }
        self.post_token_request(data)

    def post_token_request(self, data):
        """Generalized token request handling."""
        headers = {
            'Authorization': 'Basic %s' % base64.b64encode(
                f"{self.config.app_key}:{self.config.app_secret}".encode()).decode(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(f"{self.config.api_base_url}/v1/oauth/token", 
                                    headers=headers, 
                                    data=data)
        if response.status_code == 200:
            self.save_token(response.json())
            self.logger.info("Tokens successfully updated.")
            return True
        self.logger.error("Failed to obtain tokens.")
        response.raise_for_status()

    def refresh_access_token(self):
        """Use the refresh token to obtain a new access token and validate it."""
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.token_info['refresh_token']
        }
        if not self.post_token_request(data):
            self.logger.error("Failed to refresh access token.")
            self.manual_authorization_flow()
        self.token_info = self.load_token()
        return self.validate_token()

    def save_token(self, token_data):
        """Save token data securely."""
        token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
        with open(f'schwab_token_data_{self.initials}.json', 'w', encoding='utf-8') as f:
            json.dump(token_data, f)
        self.logger.info("Token data saved successfully.")

    def load_token(self):
        """Load token data."""
        try:
            with open(f'schwab_token_data_{self.initials}.json', 'r', encoding='utf-8') as f:
                token_data = json.load(f)
                return token_data
        except FileNotFoundError as e:
            self.logger.warning("Loading token failed: %s", e)
        except json.JSONDecodeError as e:
            self.logger.warning("Error decoding token file: %s", e)
        return None

    def validate_token(self, force=False):
        """Validate the current token."""
        if self.token_info and datetime.now() < datetime.fromisoformat(self.token_info['expires_at']):
            print(f"Token expires in {(datetime.fromisoformat(self.token_info['expires_at']) - datetime.now()).seconds} seconds")
            return True
        if force:
            print("Token expired or invalid.")
            params = {'symbol': 'AAPL'}
            response = self.make_request(endpoint=f"{self.config.market_data_base_url}/chains", params=params,
                                        validating=True)
            print(response)
            if response:
                self.logger.info("Token validated successfully.")
                return True
        self.logger.warning("Token validation failed.")
        return False

    def make_request(self, endpoint, method="GET", **kwargs):
        """
        Make authenticated HTTP requests.

        Args:
            endpoint (str): The API endpoint.
            method (str, optional): The HTTP method. Defaults to "GET".
            **kwargs: Additional parameters for the request.

        Returns:
            dict: The JSON response from the API if available, else None.

        Raises:
            HTTPError: If the request fails.
        """
        sleep(0.5 + random.randint(0, 1000) / 1000)

        if 'validating' not in kwargs:
            if not self.validate_token():
                self.logger.info("Token expired or invalid, re-authenticating.")
                self.refresh_access_token()
        kwargs.pop('validating', None)

        if self.config.api_base_url not in endpoint:
            url = f"{self.config.api_base_url}{endpoint}"
        else:
            url = endpoint

        self.logger.debug("Making request to %s with method %s and kwargs %s", url, method, kwargs)

        headers = {'Authorization': f'Bearer {self.token_info["access_token"]}'}

        response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:
            self.logger.warning("Token expired during request. Refreshing token...")
            self.refresh_access_token()
            headers = {'Authorization': f'Bearer {self.token_info["access_token"]}'}
            response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code != 200:
            order_pattern = r"https://api\.schwabapi\.com/trader/v1/accounts/.*/orders"
            if response.status_code == 201 and re.match(order_pattern, url):
                location = response.headers.get('location')
                if location:
                    order_id = location.split('/')[-1]
                    self.logger.debug("Order placed successfully. Order ID: %s", order_id)
                    return {"order_id": order_id, "success": True}
                self.logger.error("201 response without a location header.")
                return None

        response.raise_for_status()

        if response.content:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                self.logger.error("Error decoding JSON response: %s", e)
                raise requests.exceptions.JSONDecodeError(e.msg, e.doc, e.pos)
        self.logger.debug("Empty response content")
        return None

    def get_user_preferences(self):
        """Retrieve user preferences."""
        try:
            return self.make_request(f"{self.config.trader_base_url}/userPreference")
        except requests.RequestException as e:
            self.logger.error("Failed to get user preferences: %s", e)
            return None
