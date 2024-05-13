from datetime import datetime, timedelta
from api_client import APIClient
from accounts import Accounts
from market_data import Quotes, Options, PriceHistory, Movers, MarketHours, Instruments
from orders import Orders
from stream_client import StreamClient
from asyncio import get_event_loop


async def main_stream():
    client = APIClient()  # Initialize the API client
    stream_client = StreamClient(client)
    await stream_client.start()


def main():
    client = APIClient()  # Initialize the API client
    accounts_api = Accounts(client)
    orders_api = Orders(client)

    # Get account numbers for linked accounts
    # print(accounts_api.get_account_numbers())  # working

    # Get positions for linked accounts
    # print(accounts_api.get_all_accounts())  # working

    sample_account = client.account_numbers[0]
    account_hash = sample_account['accountHash']

    # Get specific account positions
    # print(accounts_api.get_account(fields="positions"))

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
    print(orders_api.get_orders(account_hash=account_hash, max_results=3000, from_entered_time=datetime.now() - timedelta(days=7), to_entered_time=datetime.now()))

    # Get all transactions for an account
    print(accounts_api.get_account_transactions('account_hash', datetime.now() - timedelta(days=7), datetime.now(),
                                                "TRADE").json())

    # Market-data-related requests
    quotes = Quotes(client)
    options = Options(client)
    price_history = PriceHistory(client)
    movers = Movers(client)
    market_hours = MarketHours(client)
    instruments = Instruments(client)

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
    print("Welcome to the unofficial Schwab API interface!\n"
          "GitHub: https://github.com/Patch-Code-Prosperity/Pythonic-Schwab-API")
    loop = get_event_loop()
    loop.run_until_complete(main_stream())
    # main()
