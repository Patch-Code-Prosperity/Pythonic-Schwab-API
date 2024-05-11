class Accounts:
    def __init__(self, client):
        self.client = client

    def get_account_numbers(self):
        """Retrieve account numbers associated with the user's profile."""
        return self.client.get('/trader/v1/accounts/accountNumbers')

    def get_all_accounts(self, fields=None):
        """Retrieve detailed information for all linked accounts, optionally filtering the fields."""
        params = {'fields': fields} if fields else {}
        return self.client.get('/trader/v1/accounts', params=params)

    def get_account(self, account_hash=None, fields=None):
        """Retrieve detailed information for a specific account using its hash."""
        endpoint = f'/trader/v1/accounts/{account_hash}'
        params = {'fields': fields} if fields else {}
        return self.client.get(endpoint, params=params)

    def get_account_transactions(self, account_hash, start_date, end_date, types=None, symbol=None):
        """Retrieve transactions for a specific account over a specified date range."""
        params = {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'types': types,
            'symbol': symbol
        }
        endpoint = f'/trader/v1/accounts/{account_hash}/transactions'
        return self.client.get(endpoint, params=params)
      
