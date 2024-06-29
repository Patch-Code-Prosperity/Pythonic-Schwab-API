"""
This is an example of how to use various functions/classes in the repo.
This is beyond not financial advice.
This is for demonstration purposes only.
Please do not ping me if you hook this chat-gpt-looking code up to 
a real brokerage account and just 'letterrip.'

This module demonstrates a simple trading algorithm using the Schwab API.
It includes functions to place trades, check account status, and manage orders.
"""

import json
from datetime import datetime, timedelta
import urllib.parse as urll
import pandas as pd
from tqdm import tqdm

from pythonic_schwab_api.accounts import Accounts
from pythonic_schwab_api.api_client import APIClient
from pythonic_schwab_api.orders import Orders
from pythonic_schwab_api.market_data import Quotes


def actually_do_some_trading(orders_api, account_hash, valid_quotes):
    """
    Places buy orders for valid quotes and logs the trades.

    Args:
        orders_api (Orders): The Orders API instance.
        account_hash (str): The account hash.
        valid_quotes (pd.DataFrame): DataFrame containing valid quotes for trading.

    Returns:
        list: List of tickers that were traded.
    """
    traded_tickers = []
    for ticker, row in tqdm(valid_quotes.iterrows(),
                            total=valid_quotes.shape[0],
                            desc="Processing trades"):
        bid_price = row['bidPrice']
        ask_price = row['askPrice']
        last_price = row['lastPrice']
        print(f"{ticker}")
        print(f"Bid price: {bid_price} | Ask price: {ask_price} | Last price: {last_price}")

        try:
            response = orders_api.place_order(
                account_hash=account_hash,
                symbol=ticker,
                side='BUY',
                quantity=6,
                order_type='LIMIT',
                limit_price=bid_price + 0.01,
                time_in_force='DAY'
            )
            print(f"Order response: {response}")
            try:
                with open(f"algo_trades_{orders_api.client.config.initials}.json",
                        "r", encoding="utf-8") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = []
            data.append({"ticker": ticker, "order_number": response['order_number']})
            with open(f"algo_trades_{orders_api.client.config.initials}.json",
                    "w", encoding="utf-8") as f:
                json.dump(data, f)
            traded_tickers.append(ticker)
        except (ConnectionError, TimeoutError) as e:
            print(f"Network-related error placing order: {e}")
        except ValueError as e:
            print(f"Value error placing order: {e}")
        except KeyError as e:
            print(f"Key error placing order: {e}")
        except Exception as e:
            print(f"Unexpected error placing order: {e}")
    return traded_tickers


def find_trades_from_quotes(quotes):
    """
    Filters quotes to find valid trades based on predefined criteria.

    Args:
        orders_api (Orders): The Orders API instance.
        quotes (dict): Dictionary of quotes.
        account_hash (str): The account hash.

    Returns:
        pd.DataFrame: DataFrame containing valid quotes for trading.
    """
    if not quotes or len(quotes) == 0:
        print("No quotes found.")
        return
    # Convert quotes to DataFrame
    quotes_df = pd.DataFrame.from_dict(quotes, orient='index')
    quotes_df.index = quotes_df.index.map(urll.unquote)

    # Extract relevant quote data
    quotes_df = quotes_df['quote'].apply(pd.Series)

    # Filter out quotes with missing data
    quotes_df = quotes_df.dropna(subset=['askPrice', 'askSize', 'bidPrice', 'bidSize', 'lastPrice'])

    if 'regular' not in quotes_df.columns:
        return

    valid_quotes = quotes_df[
        (quotes_df['lastPrice'] >= 0.005) &
        (quotes_df['lastPrice'] <= 0.515) &
        ((quotes_df['askPrice'] - quotes_df['bidPrice']) >= 0.06) &
        (quotes_df['regular']['regularMarketLastPrice'] / (quotes_df['askPrice'] - quotes_df['bidPrice']) <= 10) &
        (quotes_df['askSize'] <= 100) &
        (quotes_df['bidSize'] <= 100) &
        ((quotes_df['lastPrice'] - quotes_df['bidPrice']) >= 0) &
        ((quotes_df['lastPrice'] - quotes_df['askPrice']) >= 0) &
        ((quotes_df['lastPrice'] - quotes_df['bidPrice']) <= 0.7 * (quotes_df['askPrice'] - quotes_df['bidPrice'])) &
        ((quotes_df['lastPrice'] - quotes_df['askPrice']) <= 0.7 * (quotes_df['askPrice'] - quotes_df['bidPrice']))
    ]
    return valid_quotes


def sell_the_algo_buys(orders_api, account_hash, quotes_api):
    # Check order statuses and handle new trades
    try:
        with open(f"algo_trades_{orders_api.client.config.initials}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data_tickers = [trade['ticker'] for trade in data]
    data_quotes = quotes_api.get_list(data_tickers)
    all_orders = orders_api.get_orders(
        account_hash=account_hash,
        maxResults=3000,
        fromEnteredTime=(datetime.now() - timedelta(days=360)).isoformat(timespec='seconds'),
        toEnteredTime=datetime.now().isoformat(timespec='seconds')
    )
    for trade in data:
        try:
            response = all_orders.get(trade['order_number'])
            print(f"Order status for {trade['ticker']}: {response['status']}")
            bought_price = response['price']
            if response['status'] in ['FILLED', 'PARTIAL']:
                new_quote = data_quotes.get(trade['ticker'])
                new_quote_data = new_quote.get("quote")
                if new_quote_data:
                    ask_price = new_quote_data.get('askPrice')
                    if ask_price and bought_price <= ask_price - 0.03:
                        response = orders_api.place_order(
                            account_hash=account_hash,
                            symbol=trade['ticker'],
                            side='SELL',
                            quantity=1,
                            order_type='LIMIT',
                            limit_price=ask_price - 0.01,
                            time_in_force='DAY'
                        )
                        print(f"Order response: {response}")
                print(f"Order response: {response}")
        except KeyError as e:
            print(f"Key error checking order status: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Unexpected error checking order status: {e}")


def check_cash_account(account_api, account_hash):
    account = account_api.get_account(account_hash=account_hash, fields="positions")
    # print(account)
    cash_account = account["securitiesAccount"]["type"] == "CASH"
    return cash_account


def main():
    # Initialize client
    client = APIClient(initials=input("Enter your initials: "))
    accounts_api = Accounts(client)
    orders_api = Orders(client)
    quotes_api = Quotes(client)

    # Get account hash
    sample_account = client.account_numbers[0]
    account_hash = sample_account['hashValue']

    # Check cash account
    if not check_cash_account(accounts_api, account_hash):
        print("Confirm pattern day trader status or using a cash account.")
        return

    # Get quotes
    quotes = quotes_api.get_quotes(['AAPL', 'MSFT', 'GOOGL'])

    # Find valid trades
    valid_quotes = find_trades_from_quotes(quotes)

    if valid_quotes is not None and not valid_quotes.empty:
        # Place trades
        traded_tickers = actually_do_some_trading(orders_api, account_hash, valid_quotes)
        print(f"Traded tickers: {traded_tickers}")

        # Sell the algo buys
        sell_the_algo_buys(orders_api, account_hash, quotes_api)
    else:
        print("No valid trades found.")


if __name__ == "__main__":
    main()
