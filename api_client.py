import requests
import logging
import json
from datetime import datetime, timedelta
from config import APIConfig


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.setup_logging()

        if not self.validate_credentials():
            logging.error("Invalid or missing credentials. Please check your configuration.")
            exit(1)

        self.token_info = self.load_token() or self.authenticate()

    def setup_logging(self):
        logging.basicConfig(**APIConfig.LOGGING_CONFIG)
        self.logger = logging.getLogger(__name__)

    def validate_credentials(self):
        return all([APIConfig.APP_KEY, APIConfig.APP_SECRET, APIConfig.CALLBACK_URL])

    def authenticate(self):
        """Authenticate with the API and store the new token information."""
        data = {
            'grant_type': 'client_credentials',
            'client_id': APIConfig.APP_KEY,
            'client_secret': APIConfig.APP_SECRET
        }
        response = self.session.post(f"{APIConfig.API_BASE_URL}/v1/oauth/token", data=data)
        response.raise_for_status()
        token_data = response.json()
        self.save_token(token_data)
        return token_data

    def save_token(self, token_data):
        """Saves the token data securely to a file."""
        token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
        with open('token_data.json', 'w') as f:
            json.dump(token_data, f)
        self.logger.info("Token data saved successfully.")

    def load_token(self):
        """Loads the token data from a file if it is still valid."""
        try:
            with open('token_data.json', 'r') as f:
                token_data = json.load(f)
                if datetime.now() < datetime.fromisoformat(token_data['expires_at']):
                    self.logger.info("Token loaded successfully from file.")
                    return token_data
        except (FileNotFoundError, KeyError, ValueError) as e:
            self.logger.warning(f"Loading token failed: {e}")
        return None

    def make_request(self, method, endpoint, **kwargs):
        """Makes an HTTP request using the authenticated session."""
        url = f"{APIConfig.API_BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:  # Token expired
            self.logger.warning("Token expired. Refreshing token...")
            self.token_info = self.authenticate()
            response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
