import random
from time import sleep
import requests
import webbrowser
import base64
import json
from datetime import datetime, timedelta
import logging
from config import APIConfig
from color_print import ColorPrint


class APIClient:
    def __init__(self):
        self.account_numbers = None
        self.config = APIConfig
        self.session = requests.Session()
        self.setup_logging()
        self.token_info = self.load_token()

        # Validate and refresh token or reauthorize if necessary
        if not self.token_info or not self.ensure_valid_token():
            self.manual_authorization_flow()

    def setup_logging(self):
        logging.basicConfig(**APIConfig.LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)

    def ensure_valid_token(self):
        """Ensure the token is valid, refresh if possible, otherwise prompt for reauthorization."""
        if self.token_info:
            if self.validate_token():
                self.logger.info("Token loaded and valid.")
                return True
            elif 'refresh_token' in self.token_info:
                self.logger.info("Access token expired. Attempting to refresh.")
                if self.refresh_access_token():
                    return True
        self.logger.warning("Token invalid and could not be refreshed.")
        return False

    def manual_authorization_flow(self):
        """ Handle the manual steps required to get the authorization code from the user. """
        self.logger.info("Starting manual authorization flow.")
        auth_url = f"{APIConfig.API_BASE_URL}/v1/oauth/authorize?client_id={APIConfig.APP_KEY}&redirect_uri={APIConfig.CALLBACK_URL}&response_type=code"
        webbrowser.open(auth_url)
        self.logger.info(f"Please authorize the application by visiting: {auth_url}")
        response_url = ColorPrint.input(
            "After authorizing, wait for it to load (<1min) and paste the WHOLE url here: ")
        authorization_code = f"{response_url[response_url.index('code=') + 5:response_url.index('%40')]}@"
        # session = response_url[response_url.index("session=")+8:]
        self.exchange_authorization_code_for_tokens(authorization_code)

    def exchange_authorization_code_for_tokens(self, code):
        """ Exchange the authorization code for access and refresh tokens. """
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.config.CALLBACK_URL
        }
        self.post_token_request(data)

    def post_token_request(self, data):
        """ Generalized token request handling. """
        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{self.config.APP_KEY}:{self.config.APP_SECRET}".encode()).decode()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.session.post(f"{self.config.API_BASE_URL}/v1/oauth/token", headers=headers, data=data)
        if response.status_code == 200:
            self.save_token(response.json())
            self.logger.info("Tokens successfully updated.")
            return True
        else:
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
            return False
        self.token_info = self.load_token()
        return self.validate_token()

    def save_token(self, token_data):
        """ Save token data securely. """
        token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
        with open('token_data.json', 'w') as f:
            json.dump(token_data, f)
        self.logger.info("Token data saved successfully.")

    def load_token(self):
        """ Load token data. """
        try:
            with open('token_data.json', 'r') as f:
                token_data = json.load(f)
                return token_data
        except Exception as e:
            self.logger.warning(f"Loading token failed: {e}")
        return None

    def validate_token(self, force=False):
        """ Validate the current token's validity. """
        print(self.token_info['expires_at'])
        print(datetime.now())
        print(datetime.fromisoformat(self.token_info['expires_at']))
        print(datetime.now() < datetime.fromisoformat(self.token_info['expires_at']))
        if self.token_info and datetime.now() < datetime.fromisoformat(self.token_info['expires_at']):
            print(f"Token expires in {datetime.fromisoformat(self.token_info['expires_at']) - datetime.now()} seconds")
            return True
        elif force:
            print("Token expired or invalid.")
            # get AAPL to validate token
            params = {'symbol': 'AAPL'}
            response = self.make_request(endpoint=f"{self.config.MARKET_DATA_BASE_URL}/chains", params=params, validating=True)
            print(response)
            if response:
                self.logger.info("Token validated successfully.")
                # self.account_numbers = response.json()
                return True
        self.logger.warning("Token validation failed.")
        return False

    def make_request(self, endpoint, method="GET", **kwargs):
        sleep(0.5 + random.randint(0, 1000) / 1000)
        """ Make authenticated HTTP requests. """
        if 'validating' not in kwargs:
            if not self.validate_token():
                self.logger.info("Token expired or invalid, re-authenticating.")
                self.manual_authorization_flow()
        kwargs.pop('validating', None)
        if self.config.API_BASE_URL not in endpoint:
            url = f"{self.config.API_BASE_URL}{endpoint}"
        else:
            url = endpoint
        print(f"Making request to {url} with method {method} and kwargs {kwargs} (validating already popped if present)")
        headers = {'Authorization': f"Bearer {self.token_info['access_token']}"}
        response = self.session.request(method, url, headers=headers, **kwargs)
        print(response.status_code)
        print(response.text)
        if response.status_code == 401:
            self.logger.warning("Token expired during request. Refreshing token...")
            self.manual_authorization_flow()
            headers = {'Authorization': f"Bearer {self.token_info['access_token']}"}
            response = self.session.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_user_preferences(self):
        """Retrieve user preferences."""
        try:
            return self.make_request(f'{self.config.TRADER_BASE_URL}/userPreference')
        except Exception as e:
            self.logger.error(f"Failed to get user preferences: {e}")
            return None
