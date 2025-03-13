from .products import ShoperProducts
import config, json
import pandas as pd
from datetime import datetime

class ShoperSpecialOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.products = ShoperProducts(client)

    def create_special_offer(self, discount_data):
        """Create a special offer for a product.
        Args:
            discount_data (dict): Data about the discount:
                product_id: integer,
                discount: float,
                discount_type: integer, (2 - fixed, 3 - percentage),

        Returns:
            int|None: Special offer ID if successful, None if failed
        """
        today = datetime.today().strftime('%Y-%m-%d')

        params = {
            'product_id': discount_data['product_id'],
            'discount': discount_data['discount'],
            'discount_type': discount_data['discount_type'],
            'date_from': today,
            'date_to': config.PROMO_TIME_END,
        }
        
        url = f'{config.SHOPER_SITE_URL}/webapi/rest/specialoffers'

        response = self.client._handle_request('POST', url, json=params)

        if response.status_code == 200:
            print(f'✅ Special offer {params['product_id']} created.')
            return response.json()
        else:
            print(f'❌ Failed to create a special offer {params['product_id']}: {response.json()['error_description']}')


    def remove_special_offer_from_product(self, identifier, use_code=False):
        """Remove a special offer for a product.
        Args:
            identifier (int|str): Product ID or code (SKU)
            use_code (bool): Use product code (SKU) instead of product ID
        Returns:
            bool: True if successful, False if failed
        """
        if use_code:
            promo_id = self.products.get_product_by_code(identifier, use_code=True)['special_offer']['promo_id']
        else:
            product = self.products.get_product_by_code(identifier)
            promo_id = product.get('special_offer', {}).get('promo_id')

        if promo_id:
            url = f'{config.SHOPER_SITE_URL}/webapi/rest/specialoffers/{promo_id}'
            response = self.client._handle_request('DELETE', url)

            if response.status_code == 200:
                print(f'✅ Special offer {promo_id} removed successfully.')
                return True
            else:
                print(f'❌ Special offer {promo_id} removal failed. {response.json()['error_description']}')
                return False
