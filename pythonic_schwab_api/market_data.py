import datetime
import urllib.parse as urll


class Quotes:
    def __init__(self, client):
        self.client = client
        self.base_url = client.config.MARKET_DATA_BASE_URL

    def get_list(self, symbols=None, fields=None, indicative=False):
        params = {
            'symbols': ','.join(symbols) if symbols else None,
            'fields': fields,
            'indicative': indicative
        }
        return self.client.make_request(f"{self.base_url}/quotes", params=params)

    def get_single(self, symbol_id, fields=None):
        params = {'fields': fields}
        if urll.unquote(symbol_id) == symbol_id:
            symbol_id = urll.quote(symbol_id)
        return self.client.make_request(f"{self.base_url}/{symbol_id}/quotes", params=params)


class Options:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/chains"

    def get_chains(self, symbol, **kwargs):
        params = {'symbol': symbol, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class PriceHistory:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/pricehistory"

    def by_symbol(self, symbol, **kwargs):
        params = {'symbol': symbol, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class Movers:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/movers"

    def get_movers(self, index, **kwargs):
        params = {'index': index, **kwargs}
        return self.client.make_request(self.base_url, params=params)


class MarketHours:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/markets"

    def by_markets(self, markets, date=None):
        if not date:
            date = datetime.date.today().isoformat()
        params = {'markets': markets, 'date': date}
        return self.client.make_request(self.base_url, params=params)

    def by_market(self, market_id, date=None):
        if not date:
            date = datetime.date.today().isoformat()
        params = {'date': date}
        return self.client.make_request(f"{self.base_url}/{market_id}", params=params)


class Instruments:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.MARKET_DATA_BASE_URL}/instruments"

    def by_symbol(self, symbol, projection):
        params = {'symbol': symbol, 'projection': projection}
        return self.client.make_request(self.base_url, params=params)

    def by_cusip(self, cusip_id):
        return self.client.make_request(f"{self.base_url}/{cusip_id}")