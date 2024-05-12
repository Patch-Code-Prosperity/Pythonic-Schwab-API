import json
from datetime import datetime
import logging
from config import APIConfig

class APIClient:
    def __init__(self):
        self.config = APIConfig
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(**self.config.LOGGING_CONFIG)
        self.token_info = self.load_token() or self.authenticate()

    def authenticate(self):
        """ Authenticates with the API and stores the new token information. """
        self.logger.info("Authenticating with API to retrieve new tokens.")
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.config.APP_KEY,
            'client_secret': self.config.APP_SECRET
        }
        response = self.session.post(f"{self.config.API_BASE_URL}/v1/oauth/token", data=data)
        response.raise_for_status()
        token_data = response.json()
        self.save_token(token_data)
        return token_data

    def save_token(self, token_data):
        """ Saves the token data securely to a file. """
        token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
        with open('token_data.json', 'w') as f:
            json.dump(token_data, f)
        self.logger.info("Token data saved successfully.")

    def load_token(self):
        """ Loads the token data from a file if it is still valid. """
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
        """ Makes an HTTP request using the authenticated session. """
        url = f"{self.config.API_BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:  # Token expired
            self.logger.warning("Token expired. Refreshing token...")
            self.token_info = self.authenticate()
            response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
