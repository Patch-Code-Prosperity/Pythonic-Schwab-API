class Quotes:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/quotes"

    def get_list(self, symbols=None, fields=None, indicative=False):
        params = {
            'symbols': ','.join(symbols) if symbols else None,
            'fields': fields,
            'indicative': indicative
        }
        return self.client.get(self.base_url, params=params)

    def get_single(self, symbol_id, fields=None):
        params = {'fields': fields}
        return self.client.get(f"{self.base_url}/{symbol_id}", params=params)

class Options:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/chains"

    def get_chains(self, symbol, **kwargs):
        params = {'symbol': symbol, **kwargs}
        return self.client.get(self.base_url, params=params)

class PriceHistory:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/pricehistory"

    def by_symbol(self, symbol, **kwargs):
        params = {'symbol': symbol, **kwargs}
        return self.client.get(self.base_url, params=params)

class Movers:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/movers"

    def get_movers(self, index, **kwargs):
        params = {'index': index, **kwargs}
        return self.client.get(self.base_url, params=params)

class MarketHours:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/markets"

    def by_markets(self, markets, date):
        params = {'markets': markets, 'date': date}
        return self.client.get(self.base_url, params=params)

    def by_market(self, market_id, date):
        params = {'date': date}
        return self.client.get(f"{self.base_url}/{market_id}", params=params)

class Instruments:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = f"{base_url}/instruments"

    def by_symbol(self, symbol, projection):
        params = {'symbol': symbol, 'projection': projection}
        return self.client.get(self.base_url, params=params)

    def by_cusip(self, cusip_id):
        return self.client.get(f"{self.base_url}/{cusip_id}")
