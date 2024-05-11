from config import TRADER_BASE_URL
import logging

class Accounts:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.base_url = TRADER_BASE_URL

    def get_account_numbers(self):
        """Retrieve account numbers associated with the user's profile."""
        try:
            return self.client.get(f'{self.base_url}/accountNumbers')
        except Exception as e:
            self.logger.error(f"Failed to get account numbers: {e}")
            return None

    def get_all_accounts(self, fields=None):
        """Retrieve detailed information for all linked accounts, optionally filtering the fields."""
        params = {'fields': fields} if fields else {}
        try:
            return self.client.get(f'{self.base_url}', params=params)
        except Exception as e:
            self.logger.error(f"Failed to get all accounts: {e}")
            return None

    def get_account(self, account_hash, fields=None):
        """Retrieve detailed information for a specific account using its hash."""
        if not account_hash:
            self.logger.error("Account hash is required for getting account details")
            return None
        params = {'fields': fields} if fields else {}
        try:
            return self.client.get(f'{self.base_url}/{account_hash}', params=params)
        except Exception as e:
            self.logger.error(f"Failed to get account {account_hash}: {e}")
            return None

    def get_account_transactions(self, account_hash, start_date, end_date, types=None, symbol=None):
        """Retrieve transactions for a specific account over a specified date range."""
        if not (isinstance(start_date, datetime.datetime) and isinstance(end_date, datetime.datetime)):
            self.logger.error("Invalid date format. Dates must be datetime objects")
            return None
        params = {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'types': types,
            'symbol': symbol
        }
        try:
            return self.client.get(f'{self.base_url}/{account_hash}/transactions', params=params)
        except Exception as e:
            self.logger.error(f"Failed to get transactions for account {account_hash}: {e}")
            return None
