# api_client.py
import requests
from .credentials import Credentials
from .tokens import TokenManager
from .api_utilities import ParameterParser
from .config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.setup_session()

    def setup_session(self):
        """Prepare the session with necessary headers and auth setup."""
        token = TokenManager.get_access_token()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    def make_request(self, method, endpoint, params=None, data=None):
        """General method to make HTTP requests."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, params=ParameterParser.clean_params(params), json=data)
            response.raise_for_status()  # Will raise an HTTPError for bad requests
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}

    def refresh_tokens(self):
        """Handle token refresh logic."""
        new_tokens = TokenManager.refresh_tokens()
        if new_tokens:
            self.setup_session()  # Update session with new tokens

    def get(self, endpoint, params=None):
        """Wrapper for GET requests."""
        return self.make_request('GET', endpoint, params=params)

    def post(self, endpoint, data=None):
        """Wrapper for POST requests."""
        return self.make_request('POST', endpoint, data=data)

    def put(self, endpoint, data=None):
        """Wrapper for PUT requests."""
        return self.make_request('PUT', endpoint, data=data)

    def delete(self, endpoint, params=None):
        """Wrapper for DELETE requests."""
        return self.make_request('DELETE', endpoint, params=params)
