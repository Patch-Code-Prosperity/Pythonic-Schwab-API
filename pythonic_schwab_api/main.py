"""
This module provides an interface to interact with the Schwab API.
It includes functionalities for account management, order placement,
market data retrieval, and streaming data.

Classes:
    APIClient: Handles API client initialization and authentication.
    Accounts: Manages account-related operations.
    Orders: Manages order-related operations.
    Quotes: Retrieves market quotes.
    Options: Retrieves options data.
    PriceHistory: Retrieves historical price data.
    Movers: Retrieves market movers data.
    MarketHours: Retrieves market hours information.
    Instruments: Retrieves instrument information.
    StreamClient: Manages streaming data connections.

Functions:
    main_stream: Asynchronously runs the main stream functionality.
    main: Entry point for demonstrating various API operations.
"""

import asyncio
from datetime import datetime, timedelta
from asyncio import get_event_loop

from pythonic_schwab_api.api_client import APIClient
from pythonic_schwab_api.accounts import Accounts
from pythonic_schwab_api.market_data import Quotes, Options, PriceHistory, Movers, MarketHours, Instruments
from pythonic_schwab_api.orders import Orders
from pythonic_schwab_api.stream_client import StreamClient
from pythonic_schwab_api import stream_utilities


async def main_stream():
    """
    Asynchronously runs the main stream functionality.
    Creates an API client and a stream client, then starts and connects
    to the stream. Constructs and sends a subscription request for
    LEVELONE_EQUITIES with specific fields. Sends the request, waits
    for a message, prints the received message, and then delays for
    1 second between messages. Stops the stream client when the loop ends.
    """
    initials = "AB"
    client = APIClient(initials=initials)  # Initialize the API client
    stream_client = StreamClient(client)
    await stream_client.start()  # Start and connect

    while stream_client.active:
        # Construct and send a subscription request
        request = stream_utilities.basic_request(
            "LEVELONE_EQUITIES",
            request_id=stream_client.request_id,
            command="SUBS",
            customer_id=stream_client.streamer_info.get("schwabClientCustomerId"),
            correl_id=stream_client.streamer_info.get("schwabClientCorrelId"),
            parameters={
                "keys": "TSLA,AMZN,AAPL,NFLX,BABA",
                "fields": "0,1,2,3,4,5,8,9,12,13,15,24,28,29,30,31,48"
            }
        )
        await stream_client.send(request)
        message = await stream_client.receive()
        print(f"Received: {message}")
        await asyncio.sleep(1)  # Delay between messages

    stream_client.stop()


def main():
    """
    Main function that serves as the entry point for demonstrating various
    API operations such as retrieving account numbers, positions, orders,
    and different market data related requests.
    """
    initials = "AB"
    client = APIClient(initials=initials)  # Initialize the API client
    accounts_api = Accounts(client)
    orders_api = Orders(client)

    # Get account numbers for linked accounts
    client.account_numbers = accounts_api.get_account_numbers()  # working
    print(client.account_numbers)

    # Get positions for linked accounts
    print(accounts_api.get_all_accounts())  # working

    sample_account = client.account_numbers[0]  # working
    print(sample_account)
    account_hash = sample_account['hashValue']  # working
    print(account_hash)

    # Get specific account positions
    print(accounts_api.get_account(account_hash=account_hash, fields="positions"))

    # Get up to 3000 orders for an account for the past week
    print(orders_api.get_orders(account_hash=account_hash,
                                max_results=3000,
                                from_entered_time=datetime.now() - timedelta(days=7),
                                to_entered_time=datetime.now())
        )

    # # Example to place an order (commented out for safety)
    # order_details = {
    #     "orderType": "LIMIT",
    #     "session": "NORMAL",
    #     "duration": "DAY",
    #     "orderStrategyType": "SINGLE",
    #     "price": '10.00',
    #     "orderLegCollection": [
    #         {"instruction": "BUY", "quantity": 1,
    #         "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}
    #     ]
    # }
    # order_response = orders_api.place_order('account_hash', order_details)
    # print(f"Place order response: {order_response.json()}")
    # order_id = order_response.headers.get('location', '/').split('/')[-1]

    # Get a specific order
    # print(orders_api.get_order('account_hash', order_id).json())

    # Get up to 3000 orders for all accounts for the past week
    for account in client.account_numbers:
        account_hash = account['hashValue']
        print(orders_api.get_orders(
            account_hash=account_hash, max_results=3000,
            from_entered_time=datetime.now() - timedelta(days=7),
            to_entered_time=datetime.now()))

    # Get all transactions for an account
    print(
        accounts_api.get_account_transactions(
            account_hash=account_hash,
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now(),
            types="TRADE")
        )

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

    # Get price history for a symbol
    print(
        price_history.by_symbol(
            "AAPL", period_type="day", period=1, 
            frequency_type="minute",
            frequency=5).json()
        )

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
    main()
    loop = get_event_loop()
    loop.run_until_complete(main_stream())
    loop.close()
