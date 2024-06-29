"""
This module provides classes to interact with market data endpoints of the Schwab API.
"""

import datetime
import urllib.parse as urll


class Quotes:
    """
    A class to retrieve quotes for symbols.
    """
    def __init__(self, client):
        """
        Initialize the Quotes class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = client.config.MARKET_DATA_BASE_URL

    def get_list(self, symbols=None, fields=None, indicative=False):
        """
        Get a list of quotes for the given symbols.

        :param symbols: List of symbols to get quotes for.
        :param fields: Fields to include in the response.
        :param indicative: Whether to include indicative quotes.
        :return: Response from the API.
        """
        params = {
            'symbols': ','.join(symbols) if symbols else None,
            'fields': fields,
            'indicative': indicative
        }
        return self.client.make_request(f"{self.base_url}/quotes", params=params)

    def get_single(self, symbol_id, fields=None):
        """
        Get a single quote for the given symbol.

        :param symbol_id: The symbol ID to get the quote for.
        :param fields: Fields to include in the response.
        :return: Response from the API.
        """
        params = {'fields': fields}
        if urll.unquote(symbol_id) == symbol_id:
            symbol_id = urll.quote(symbol_id)
        return self.client.make_request(f"{self.base_url}/{symbol_id}/quotes", params=params)


class Options:
    """
    A class to retrieve options chains.
    """
    def __init__(self, client):
        """
        Initialize the Options class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/chains"

    def get_chains(self, symbol, **kwargs):
        """
        Get options chains for the given symbol.

        :param symbol: The symbol to get options chains for.
        :param kwargs: Additional parameters for the request.
        :return: Response from the API.
        """
        params = {'symbol': symbol, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class PriceHistory:
    """
    A class to retrieve price history.
    """
    def __init__(self, client):
        """
        Initialize the PriceHistory class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/pricehistory"

    def by_symbol(self, symbol, **kwargs):
        """
        Get price history for the given symbol.

        :param symbol: The symbol to get price history for.
        :param kwargs: Additional parameters for the request.
        :return: Response from the API.
        """
        params = {'symbol': symbol, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class Movers:
    """
    A class to retrieve market movers.
    """
    def __init__(self, client):
        """
        Initialize the Movers class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/movers"

    def get_movers(self, index, **kwargs):
        """
        Get market movers for the given index.

        :param index: The index to get movers for.
        :param kwargs: Additional parameters for the request.
        :return: Response from the API.
        """
        params = {'index': index, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class MarketHours:
    """
    A class to retrieve market hours.
    """
    def __init__(self, client):
        """
        Initialize the MarketHours class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/markets"

    def by_markets(self, markets, date=None):
        """
        Get market hours for the given markets.

        :param markets: List of markets to get hours for.
        :param date: The date to get market hours for.
        :return: Response from the API.
        """
        if not date:
            date = datetime.date.today().isoformat()
        params = {'markets': markets, 'date': date}
        return self.client.make_request(self.base_url, params=params)

    def by_market(self, market_id, date=None):
        """
        Get market hours for a single market.

        :param market_id: The market ID to get hours for.
        :param date: The date to get market hours for.
        :return: Response from the API.
        """
        if not date:
            date = datetime.date.today().isoformat()
        params = {'date': date}
        return self.client.make_request(f"{self.base_url}/{market_id}", params=params)


class Instruments:
    """
    A class to retrieve instrument information.
    """
    def __init__(self, client):
        """
        Initialize the Instruments class with a client instance.

        :param client: The client instance to make requests.
        """
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/instruments"

    def by_symbol(self, symbol, projection):
        """
        Get instrument information by symbol.

        :param symbol: The symbol to get information for.
        :param projection: The projection type for the request.
        :return: Response from the API.
        """
        params = {'symbol': symbol, 'projection': projection}
        return self.client.make_request(self.base_url, params=params)

    def by_cusip(self, cusip_id):
        """
        Get instrument information by CUSIP ID.

        :param cusip_id: The CUSIP ID to get information for.
        :return: Response from the API.
        """
        return self.client.make_request(f"{self.base_url}/{cusip_id}")
