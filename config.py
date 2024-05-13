import os
from dotenv import load_dotenv

load_dotenv()


class APIConfig:
    API_BASE_URL = "https://api.schwabapi.com"
    TRADER_BASE_URL = f"{API_BASE_URL}/trader/v1"
    MARKET_DATA_BASE_URL = f"{API_BASE_URL}/marketdata/v1"
    ORDER_BASE_URL = f"{API_BASE_URL}/accounts"
    REQUEST_TIMEOUT = 30  # Timeout for API requests in seconds
    RETRY_STRATEGY = {
        'total': 3,  # Total number of retries to allow
        'backoff_factor': 1  # Factor by which the delay between retries will increase
    }
    TOKEN_REFRESH_THRESHOLD_SECONDS = 300  # Time in seconds before token expiration to attempt refresh
    DEBUG_MODE = False
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    APP_KEY = os.getenv('APP_KEY')
    APP_SECRET = os.getenv('APP_SECRET')
    CALLBACK_URL = os.getenv('CALLBACK_URL')
