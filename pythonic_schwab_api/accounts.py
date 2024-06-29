"""
This module provides the Accounts class for interacting with account-related
endpoints of the Schwab API.

Classes:
    - Accounts: A class to handle operations related to user accounts, such as
    retrieving account numbers, detailed account information, and transactions.

Usage example:
    client = SchwabClient(api_key, secret_key)
    accounts = Accounts(client)
    account_numbers = accounts.get_account_numbers()
    all_accounts = accounts.get_all_accounts(fields=['balance', 'status'])
    specific_account = accounts.get_account(account_hash='abc123', fields=['balance'])
    transactions = accounts.get_account_transactions(
        account_hash='abc123', 
        start_date=datetime.datetime(2023, 1, 1), 
        end_date=datetime.datetime(2023, 1, 31)
        )
"""
import datetime
import logging
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout


class Accounts:
    """
    A class to handle operations related to user accounts, such as retrieving
    account numbers, detailed account information, and transactions.

    Methods:
        - get_account_numbers: Retrieve account numbers associated with the user's profile.
        - get_all_accounts: Retrieve detailed information for all linked accounts.
        - get_account: Retrieve detailed information for a specific account using its hash.
        - get_account_transactions: Retrieve transactions for a specific account
        over a specified date range.
    """
    def __init__(self, client):
        """
        Initialize the Accounts class.

        :param client: The client instance used to make API requests.
        """
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.base_url = client.config.ACCOUNTS_BASE_URL

    def get_account_numbers(self):
        """
        Retrieve account numbers associated with the user's profile.

        :return: A list of account numbers or None if the request fails.
        """
        try:
            print(f'{self.base_url}/accountNumbers')
            return self.client.make_request(f'{self.base_url}/accountNumbers')
        except (RequestException, HTTPError, ConnectionError, Timeout) as e:
            self.logger.error("Failed to get account numbers: %s", e)
            return None

    def get_all_accounts(self, fields=None):
        """
        Retrieve detailed information for all linked accounts,
        optionally filtering the fields.

        :param fields: Optional; A list of fields to filter the account information.
        :return: A list of account details or None if the request fails.
        """
        params = {'fields': fields} if fields else {}
        try:
            return self.client.make_request(f'{self.base_url}', params=params)
        except (RequestException, HTTPError, ConnectionError, Timeout) as e:
            self.logger.error("Failed to get all accounts: %s", e)
            return None

    def get_account(self, account_hash, fields=None):
        """
        Retrieve detailed information for a specific account using its hash.

        :param account_hash: The hash of the account to retrieve.
        :param fields: Optional; A list of fields to filter the account information.
        :return: Account details or None if the request fails.
        """
        if not account_hash:
            self.logger.error("Account hash is required for getting account details")
            return None
        params = {'fields': fields} if fields else {}
        try:
            return self.client.make_request(f'{self.base_url}/{account_hash}', params=params)
        except (RequestException, HTTPError, ConnectionError, Timeout) as e:
            self.logger.error("Failed to get account %s: %s", account_hash, e)
            return None

    def get_account_transactions(self, account_hash, start_date, end_date, types=None, symbol=None):
        """
        Retrieve transactions for a specific account over a specified date range.

        :param account_hash: The hash of the account to retrieve transactions for.
        :param start_date: The start date for the transaction retrieval (datetime object).
        :param end_date: The end date for the transaction retrieval (datetime object).
        :param types: Optional; A list of transaction types to filter.
        :param symbol: Optional; A specific symbol to filter transactions.
        :return: A list of transactions or None if the request fails.
        """
        if not (isinstance(start_date, datetime.datetime) and
                isinstance(end_date, datetime.datetime)):
            self.logger.error("Invalid date format. Dates must be datetime objects")
            return None
        params = {
            'startDate': start_date.isoformat(),
            'endDate': end_date.isoformat(),
            'types': types,
            'symbol': symbol
        }
        try:
            return self.client.make_request(f'{self.base_url}/{account_hash}/transactions',
                                            params=params)
        except (RequestException, HTTPError, ConnectionError, Timeout) as e:
            self.logger.error("Failed to get transactions for account %s: %s", account_hash, e)
            return None
