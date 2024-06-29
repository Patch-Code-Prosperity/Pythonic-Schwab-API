import os
from dotenv import load_dotenv

load_dotenv()
sandbox = False


class APIConfig:
    """
    Initializes the APIConfig object with the provided initials.

    Parameters:
        initials (str): The initials used for configuration.
    """
    def __init__(self, initials):
        self.initials = initials
        if sandbox:
            self.api_base_url = "http://localhost:4020"
            self.trader_base_url = self.api_base_url
            self.accounts_base_url = f"{self.api_base_url}/accounts"
            self.market_data_base_url = f"{self.api_base_url}/marketdata"
            self.orders_base_url = self.accounts_base_url
            self.streamer_info_url = f"{self.api_base_url}/streamer-info"
        else:
            self.api_base_url = "https://api.schwabapi.com"
            self.trader_base_url = f"{self.api_base_url}/trader/v1"
            self.accounts_base_url = f"{self.trader_base_url}/accounts"
            self.market_data_base_url = f"{self.api_base_url}/marketdata/v1"
            self.orders_base_url = self.accounts_base_url
            self.streamer_info_url = f"{self.api_base_url}/streamer-info"
        self.request_timeout = 30  # Timeout for API requests in seconds
        self. retry_strategy = {
            'total': 3,  # Total number of retries to allow
            'backoff_factor': 1  # Factor by which the delay between retries will increase
        }
        self.token_refresh_threshold_seconds = 300  # seconds before token expiration to attempt refresh
        self.debug_mode = False
        self.logging_config = {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
        self.app_key = os.getenv(f'SCHWAB_APP_KEY_{self.initials}')
        self.app_secret = os.getenv(f'SCHWAB_APP_SECRET_{self.initials}')
        self.callback_url = os.getenv('CALLBACK_URL')
