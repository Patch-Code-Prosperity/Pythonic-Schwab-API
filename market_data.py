class MarketData:
    def __init__(self, client):
        self.client = client
        self.base_url = "/marketdata/v1"

    class Quotes:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/quotes"

        def get_list(self, symbols=None, fields=None, indicative=False):
            """Retrieve quotes for a list of symbols."""
            params = {
                'symbols': ','.join(symbols) if symbols else None,
                'fields': fields,
                'indicative': indicative
            }
            return self.client.get(self.base_url, params=params)

        def get_single(self, symbol_id, fields=None):
            """Retrieve quote for a single symbol."""
            params = {'fields': fields}
            endpoint = f"{self.base_url}/{symbol_id}"
            return self.client.get(endpoint, params=params)

    class Options:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/chains"

        def get_chains(self, symbol, contract_type=None, strike_count=None, include_underlying_quotes=None, strategy=None, interval=None, strike=None, range=None, from_date=None, to_date=None, volatility=None, underlying_price=None, interest_rate=None, days_to_expiration=None, exp_month=None, option_type=None, entitlement=None):
            """Retrieve options chains for a symbol."""
            params = {
                'symbol': symbol,
                'contractType': contract_type,
                'strikeCount': strike_count,
                'includeUnderlyingQuotes': include_underlying_quotes,
                'strategy': strategy,
                'interval': interval,
                'strike': strike,
                'range': range,
                'fromDate': from_date,
                'toDate': to_date,
                'volatility': volatility,
                'underlyingPrice': underlying_price,
                'interestRate': interest_rate,
                'daysToExpiration': days_to_expiration,
                'expMonth': exp_month,
                'optionType': option_type,
                'entitlement': entitlement
            }
            return self.client.get(self.base_url, params=params)

    class PriceHistory:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/pricehistory"

        def by_symbol(self, symbol, period_type=None, period=None, frequency_type=None, frequency=None, start_date=None, end_date=None, need_extended_hours_data=None, need_previous_close=None):
            """Retrieve price history for a symbol."""
            params = {
                'symbol': symbol,
                'periodType': period_type,
                'period': period,
                'frequencyType': frequency_type,
                'frequency': frequency,
                'startDate': start_date,
                'endDate': end_date,
                'needExtendedHoursData': need_extended_hours_data,
                'needPreviousClose': need_previous_close
            }
            return self.client.get(self.base_url, params=params)

    class Movers:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/movers"

        def get_movers(self, index, direction='up', change='percent'):
            """Retrieve top movers of a market index."""
            params = {
                'index': index,
                'direction': direction,
                'change': change
            }
            return self.client.get(self.base_url, params=params)

    class MarketHours:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/markets"

        def by_markets(self, markets, date):
            """Retrieve market hours for specific markets on a given date."""
            params = {
                'markets': markets,
                'date': date
            }
            return self.client.get(self.base_url, params=params)

        def by_market(self, market_id, date):
            """Retrieve market hours for a specific market on a given date."""
            endpoint = f"{self.base_url}/{market_id}"
            params = {'date': date}
            return self.client.get(endpoint, params=params)

    class Instruments:
        def __init__(self, market_data):
            self.client = market_data.client
            self.base_url = f"{market_data.base_url}/instruments"

        def by_symbol(self, symbol, projection):
            """Retrieve detailed information about financial instruments by symbol."""
            params = {'symbol': symbol, 'projection': projection}
            return self.client.get(self.base_url, params=params)

        def by_cusip(self, cusip_id):
            """Retrieve detailed information about financial instruments by CUSIP ID."""
            endpoint = f"{self.base_url}/{cusip_id}"
            return self.client.get(endpoint)
