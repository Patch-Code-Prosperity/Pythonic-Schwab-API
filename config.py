import os
from dotenv import load_dotenv

load_dotenv()
SANDBOX = False


class APIConfig:
    def __init__(self, initials):
        self.initials = initials
        if SANDBOX:
            self.API_BASE_URL = "http://localhost:4020"
            self.TRADER_BASE_URL = self.API_BASE_URL
            self.ACCOUNTS_BASE_URL = f"{self.API_BASE_URL}/accounts"
            self.MARKET_DATA_BASE_URL = f"{self.API_BASE_URL}/marketdata"
            self.ORDERS_BASE_URL = self.ACCOUNTS_BASE_URL
            self.STREAMER_INFO_URL = f"{self.API_BASE_URL}/streamer-info"
        else:
            self.API_BASE_URL = "https://api.schwabapi.com"
            self.TRADER_BASE_URL = f"{self.API_BASE_URL}/trader/v1"
            self.ACCOUNTS_BASE_URL = f"{self.TRADER_BASE_URL}/accounts"
            self.MARKET_DATA_BASE_URL = f"{self.API_BASE_URL}/marketdata/v1"
            self.ORDERS_BASE_URL = self.ACCOUNTS_BASE_URL
            self.STREAMER_INFO_URL = f"{self.API_BASE_URL}/streamer-info"
        self.REQUEST_TIMEOUT = 30  # Timeout for API requests in seconds
        self. RETRY_STRATEGY = {
            'total': 3,  # Total number of retries to allow
            'backoff_factor': 1  # Factor by which the delay between retries will increase
        }
        self.TOKEN_REFRESH_THRESHOLD_SECONDS = 300  # Time in seconds before token expiration to attempt refresh
        self.DEBUG_MODE = False
        self.LOGGING_CONFIG = {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
        self.APP_KEY = os.getenv(f'SCHWAB_APP_KEY_{self.initials}')
        self.APP_SECRET = os.getenv(f'SCHWAB_APP_SECRET_{self.initials}')
        self.CALLBACK_URL = os.getenv('CALLBACK_URL')
