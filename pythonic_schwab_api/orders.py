from datetime import datetime, timezone, timedelta


class Orders:
    def __init__(self, client):
        self.client = client
        self.base_url = client.config.ORDERS_BASE_URL

    def get_orders(self, account_hash, max_results=100, from_entered_time=None, to_entered_time=None, status=None):
        """Retrieve a list of orders for a specified account."""
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

    def place_order(self, account_hash, order_details):
        """Place a new order for an account."""
        endpoint = f"{self.base_url}/{account_hash}/orders"
        return self.client.post(endpoint, data=order_details)

    def get_order(self, account_hash, order_id):
        """Retrieve details for a specific order."""
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint)

    def cancel_order(self, account_hash, order_id):
        """Cancel a specific order."""
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint, method='DELETE')

    def replace_order(self, account_hash, order_id, new_order_details):
        """Replace an existing order with new details."""
        endpoint = f"{self.base_url}/{account_hash}/orders/{order_id}"
        return self.client.make_request(endpoint, method='PUT', data=new_order_details)
