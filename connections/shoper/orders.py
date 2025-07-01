import config
from tqdm import tqdm
from utils.logger import get_outlet_logger
from datetime import datetime
import json


class ShoperOrders:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.outlet_logger = get_outlet_logger().get_logger()

    def get_latest_order_products(self, pages_to_fetch=1):
        """Get the latest order products from Shoper
        Arguments:
            pages_to_fetch (int): The number of pages to get. If None, get the first page.
        Returns:
            list: A list of order products
        """
        try:
            order_products = []
            params = {'limit': config.SHOPER_LIMIT}
            initial_response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/order-products', params=params)

            number_of_pages = initial_response.json()['pages']

            # We want to get the last 10 pages, but need to handle case where there are fewer pages
            start_page = number_of_pages
            end_page = max(1, number_of_pages - pages_to_fetch)

            for page in tqdm(range(start_page, end_page - 1, -1), desc="Downloading pages", unit=' page'):
                params['page'] = page
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/order-products', params=params)
                data = response.json()['list']
                order_products.extend(data)

            return order_products

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)

    def get_orders_by_discount_code(self, discount_code):
        """
        Fetch orders from Shoper filtered by a discount code.

        Args:
            discount_code (int or str): The discount code ID to filter orders by.

        Returns:
            dict or str: The JSON response from the API, or an error message.
        """
        try:
            orders = []
            filters = json.dumps({
                'code_id': discount_code,
            })

            params = {'limit': config.SHOPER_LIMIT, 'page': 1, 'filters': filters}
            url = f'{self.client.site_url}/webapi/rest/orders'
            response = self.client._handle_request('GET', url, params=params)

            number_of_pages = response.json()['pages']
   
            for page in tqdm(range(1, number_of_pages + 1), desc="Downloading pages", unit=' page'):
                params['page'] = page
                response = self.client._handle_request('GET', url, params=params)
                data = response.json()['list']
                orders.extend(data)

            return orders

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)