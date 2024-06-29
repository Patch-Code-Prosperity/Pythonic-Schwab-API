"""
This module provides the Orders class to interact with order-related endpoints
of the Schwab API.

The Orders class includes methods to create order schemas, place, preview,
replace, cancel, and retrieve orders for a specified account.
"""

from datetime import datetime, timezone, timedelta


class Orders:
    """
    Represents the functionality to interact with order-related endpoints of
    the Schwab API.

    Provides methods to create order schemas, place, preview, replace, cancel,
    and retrieve orders for a specified account.

    Attributes:
        client: A configured client instance used to make API requests.
        base_url: The base URL for the orders endpoint, derived from the client
                configuration.
    """
    def __init__(self, client):
        """
        Initialize the Orders class with a client instance.

        Args:
            client: A configured client instance used to make API requests.
        """
        self.client = client
        self.base_url = client.config.ORDERS_BASE_URL

    def create_order_schema(self, symbol, side, quantity, order_type='MARKET',
                            limit_price=None, time_in_force='DAY', session='NORMAL'):
        """
        Create a new order schema.

        Args:
            symbol: The symbol of the asset to be ordered.
            side: The side of the order (e.g., 'BUY' or 'SELL').
            quantity: The quantity of the asset to be ordered.
            order_type: The type of the order (default is 'MARKET').
            limit_price: The limit price for the order (if applicable).
            time_in_force: The time in force for the order (default is 'DAY').
            session: The session in which the order will be placed (default is 'NORMAL').

        Returns:
            dict: A dictionary representing the order schema.
        """
        if order_type not in ['MARKET']:
            quantity = int(quantity)
        order = {
            'orderType': order_type,
            'session': session,
            'duration': time_in_force,
            'orderStrategyType': 'SINGLE',
            'orderLegCollection': [
                {
                    'instruction': side,
                    'quantity': quantity,
                    'instrument': {
                        'symbol': symbol,
                        'assetType': 'EQUITY'
                    }
                }
            ]
        }
        if order_type == 'LIMIT':
            order['price'] = limit_price
        return order

    def get_orders(self, account_hash, max_results=100, from_entered_time=None, to_entered_time=None, status=None):
        """
        Retrieve a list of orders for a specified account.

        Args:
            account_hash: The account identifier.
            max_results: The maximum number of results to retrieve (default is 100).
            from_entered_time: The start time for the order retrieval period.
            to_entered_time: The end time for the order retrieval period.
            status: The status of the orders to retrieve.

        Returns:
            Response: The response from the API containing the list of orders.
        """
        if from_entered_time is None:
            from_entered_time = (datetime.now(timezone.utc) - timedelta(days=364)).isoformat(timespec='seconds')
        if to_entered_time is None:
            to_entered_time = datetime.now(timezone.utc).isoformat(timespec='seconds')
        params = {
            'maxResults': max_results,
            'fromEnteredTime': from_entered_time,
            'toEnteredTime': to_entered_time,
            'status': status
        }
        endpoint = f"{self.base_url}/{account_hash}/orders"
        return self.client.make_request(endpoint, params=params)

    def preview_order(self, account_hash, order_details):
        """
        Preview a new order for an account.

        Args:
            account_hash: The account identifier.
            order_details: A dictionary containing the details of the order to preview.

        Returns:
            Response: The response from the API containing the preview of the order.
        """
        # TODO: Coming Soon per the API documentation
        return "test"
        endpoint = f"{self.base_url}/{account_hash}/orders/previewOrder"
        return self.client.make_request(method="POST", endpoint=endpoint, data=order_details)

    def place_order(self, account_hash, order_details):
        """
        Place a new order for an account.

        Args:
            account_hash: The account identifier.
            order_details: A dictionary containing the details of the order to place.

        Returns:
            Response: The response from the API confirming the order placement.
        """
        endpoint = f"{self.base_url}/{account_hash}/orders"
        filtered_order_details = {k: v for k, v in order_details.items() if v is not None}
        return self.client.make_request(
            method="POST",
            endpoint=endpoint,
            json=filtered_order_details
            )

    def get_order(self, account_hash, order_id):
        """
        Retrieve details for a specific order.

        Args:
            account_hash: The account identifier.
            order_id: The identifier of the order to retrieve.

        Returns:
            Response: The response from the API containing the order details.
        """
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint)

    def cancel_order(self, account_hash, order_id):
        """
        Cancel a specific order.

        Args:
            account_hash: The account identifier.
            order_id: The identifier of the order to cancel.

        Returns:
            Response: The response from the API confirming the order cancellation.
        """
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint, method='DELETE')

    def replace_order(self, account_hash, order_id, new_order_details):
        """
        Replace an existing order with new details.

        Args:
            account_hash: The account identifier.
            order_id: The identifier of the order to replace.
            new_order_details: A dictionary containing the new details of the order.

        Returns:
            Response: The response from the API confirming the order replacement.
        """
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint, method='PUT', data=new_order_details)
