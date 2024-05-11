from modules import api, stream
from datetime import datetime, timedelta

def main():
    # Get account numbers for linked accounts
    print(api.accounts.get_account_numbers().json())

    # Get positions for linked accounts
    print(api.accounts.get_all_accounts().json())

    # Get specific account positions
    print(api.accounts.get_account(fields="positions").json())

    # Get up to 3000 orders for an account for the past week
    print(api.orders.get_orders(3000, datetime.now() - timedelta(days=7), datetime.now()).json())

    # Place an order (uncomment to test)
    """
    order = {
        "orderType": "LIMIT", 
        "session": "NORMAL", 
        "duration": "DAY", 
        "orderStrategyType": "SINGLE", 
        "price": '10.00',
        "orderLegCollection": [
            {"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}
        ]
    }
    response = api.orders.place_order(order)
    print(f"Place order response: {response}")
    order_id = response.headers.get('location', '/').split('/')[-1]
    print(f"OrderID: {order_id}")

    # Get a specific order
    print(api.orders.get_order(order_id).json())

    # Cancel specific order
    print(api.orders.cancel_order(order_id))
    """

    # Replace specific order
    # api.orders.replace_order(order_id, order)

    # Get up to 3000 orders for all accounts for the past week
    print(api.orders.get_all_orders(3000, datetime.now() - timedelta(days=7), datetime.now()).json())

    # Get all transactions for an account
    print(api.transactions.get_transactions(datetime.now() - timedelta(days=7), datetime.now(), "TRADE").json())

    # Get user preferences for an account
    print(api.user_preference.get_user_preference().json())

    # Get a list of quotes
    print(api.quotes.get_list(["AAPL", "AMD"]).json())

    # Get a single quote
    print(api.quotes.get_single("INTC").json())

    # Get an option expiration chain
    print(api.options.get_expiration_chain("AAPL").json())

    # Get movers for an index
    print(api.movers.get_movers("$DJI").json())

    # Get market hours for symbols
    print(api.market_hours.get_by_markets("equity,option").json())

    # Get market hours for a market
    print(api.market_hours.get_by_market("equity").json())

    # Get instruments for a symbol
    print(api.instruments.get_by_symbol("AAPL", "search").json())

    # Get instruments for a CUSIP
    print(api.instruments.get_by_cusip("037833100").json())  # 037833100 = AAPL

    # Send a subscription request to the stream (uncomment if you start the stream below)
    """
    stream.send(stream.utilities.basic_request("CHART_EQUITY", "SUBS", parameters={"keys": "AMD,INTC", "fields": "0,1,2,3,4,5,6,7,8"}))
    # Stop the stream after 30s
    stream.stop()
    """

if __name__ == '__main__':
    print("Welcome to the unofficial Schwab API interface!\nGitHub: https://github.com/tylerebowers/Schwab-API-Python")
    api.initialize()  # checks tokens & loads variables
    api.update_tokens_automatically()  # starts thread to update tokens automatically
    # stream.start_manual()  # start the stream manually
    main()  # call the user code above
