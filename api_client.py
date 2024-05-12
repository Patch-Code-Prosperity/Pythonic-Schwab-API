# api_client.py
import requests
import json
import logging
from datetime import datetime, timedelta
from config import API_BASE_URL, TOKEN_ENDPOINT

class APIClient:
    def __init__(self, credentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.token_info = self.load_token() or self.authenticate()

    def authenticate(self):
        """ Authenticate with the API and return the token information. """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.credentials.app_key,
            'client_secret': self.credentials.app_secret
        }
        response = self.session.post(TOKEN_ENDPOINT, data=data)
        response.raise_for_status()  # This will raise an error for non-200 responses
        token_data = response.json()
        self.save_token(token_data)
        return token_data

    def save_token(self, token_data):
        """ Save token data to a local JSON file """
        with open('token_data.json', 'w') as f:
            json.dump(token_data, f)

    def load_token(self):
        """ Load token data from a local JSON file """
        try:
            with open('token_data.json', 'r') as f:
                token_data = json.load(f)
                token_expiration = datetime.fromisoformat(token_data['expires_at'])
                if datetime.now() < token_expiration - timedelta(minutes=5):  # buffer for token expiration
                    return token_data
        except (FileNotFoundError, KeyError):
            return None

    def make_request(self, method, endpoint, **kwargs):
        """ Make an HTTP request using the authenticated session. """
        url = f"{API_BASE_URL}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:  # Token expired or not valid
            self.token_info = self.authenticate()
            response = self.session.request(method, url, **kwargs)  # Retry request
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()

    def get(self, endpoint, params=None):
        return self.make_request('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        return self.make_request('POST', endpoint, json=data)
