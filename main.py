from datetime import datetime, timedelta
from api_client import APIClient
from accounts import Accounts
from orders import Orders


def main():
    client = APIClient()  # Initialize the API client
    accounts_api = Accounts(client)
    orders_api = Orders(client)

    # Get account numbers for linked accounts
    print(accounts_api.get_account_numbers())

    # Get positions for linked accounts
    print(accounts_api.get_all_accounts().json())

    # Get specific account positions
    print(accounts_api.get_account(fields="positions").json())

    # Get up to 3000 orders for an account for the past week
    print(orders_api.get_orders(3000, datetime.now() - timedelta(days=7), datetime.now()).json())

    # Example to place an order (commented out for safety)
    """
    order_details = {
        "orderType": "LIMIT", 
        "session": "NORMAL", 
        "duration": "DAY", 
        "orderStrategyType": "SINGLE", 
        "price": '10.00',
        "orderLegCollection": [
            {"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}
        ]
    }
    order_response = orders_api.place_order('account_hash', order_details)
    print(f"Place order response: {order_response.json()}")
    order_id = order_response.headers.get('location', '/').split('/')[-1]
    """

    # Get a specific order
    # print(orders_api.get_order('account_hash', order_id).json())

    # Get up to 3000 orders for all accounts for the past week
    print(orders_api.get_orders(3000, datetime.now() - timedelta(days=7), datetime.now()).json())

    # Get all transactions for an account
    print(accounts_api.get_account_transactions('account_hash', datetime.now() - timedelta(days=7), datetime.now(),
                                                "TRADE").json())

    # Get user preferences for an account
    print(accounts_api.get_user_preferences('account_hash').json())

    # Market-data-related requests
    quotes = market_data_api.Quotes(market_data_api)
    options = market_data_api.Options(market_data_api)
    price_history = market_data_api.PriceHistory(market_data_api)
    movers = market_data_api.Movers(market_data_api)
    market_hours = market_data_api.MarketHours(market_data_api)
    instruments = market_data_api.Instruments(market_data_api)

    # Get a list of quotes
    print(quotes.get_list(["AAPL", "AMD"]).json())

    # Get a single quote
    print(quotes.get_single("INTC").json())

    # Get an option expiration chain
    print(options.get_chains("AAPL").json())

    # Get movers for an index
    print(movers.get_movers("$DJI").json())

    # Get market hours for symbols
    print(market_hours.by_markets("equity,option").json())

    # Get market hours for a market
    print(market_hours.by_market("equity").json())

    # Get instruments for a symbol
    print(instruments.by_symbol("AAPL", "search").json())

    # Get instruments for a CUSIP
    print(instruments.by_cusip("037833100").json())  # 037833100 = AAPL


if __name__ == '__main__':
    print(
        "Welcome to the unofficial Schwab API interface!\nGitHub: https://github.com/Patch-Code-Prosperity/Pythonic-Schwab-API")
    main()
