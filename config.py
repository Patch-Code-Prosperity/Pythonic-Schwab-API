# Configurations for the Schwab API client

# Base URLs for different parts of the Schwab API
API_BASE_URL = "https://api.schwabapi.com"
TRADER_BASE_URL = f"{API_BASE_URL}/trader/v1"
MARKET_DATA_BASE_URL = f"{API_BASE_URL}/marketdata/v1"
ORDER_BASE_URL = f"{API_BASE_URL}/accounts"

# Potential other configuration settings
REQUEST_TIMEOUT = 30  # Timeout for API requests in seconds
RETRY_STRATEGY = {
    'total': 3,         # Total number of retries to allow
    'backoff_factor': 1 # Factor by which the delay between retries will increase
}

# Security settings (such as token refresh thresholds, etc.)
TOKEN_REFRESH_THRESHOLD_SECONDS = 300  # Time in seconds before token expiration to attempt refresh

# Developer specific settings, like debug modes or log configurations
DEBUG_MODE = False
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
