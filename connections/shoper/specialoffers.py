from .products import ShoperProducts
import config
from datetime import datetime
from utils.logger import get_outlet_logger, get_promo_logger


class ShoperSpecialOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.products = ShoperProducts(client)
        self.outlet_logger = get_outlet_logger().get_logger()
        self.promo_logger = get_promo_logger().get_logger()

    def create_special_offer(self, discount_data):
        """Create a special offer for a product.
        Args:
            discount_data (dict): Data about the discount:
                product_id: integer,
                discount: float,
                discount_type: integer, (2 - fixed, 3 - percentage),
                date_to: dd-mm-YYYY

        Returns:
            int|None: Special offer ID if successful, None if failed
        """
        try:
            today = datetime.today().strftime('%Y-%m-%d')

            params = {
                'product_id': discount_data['product_id'],
                'discount': discount_data['discount'],
                'discount_type': discount_data['discount_type'],
                'date_from': today,
                'date_to': discount_data['date_to'],
            }
            
            url = f'{config.SHOPER_SITE_URL}/webapi/rest/specialoffers'

            response = self.client._handle_request('POST', url, json=params)

            if response.status_code == 200:
                return response.json()
            else:
                error_description = response.json()['error_description']
                self.outlet_logger.warning(f'❌ API Error: {error_description}')
                self.promo_logger.warning(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}
            
        except Exception as e:
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            self.promo_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)

    def remove_special_offer_from_product(self, identifier, use_code=False):
        """Remove a special offer for a product.
        Args:
            identifier (int|str): Product ID or code (SKU)
            use_code (bool): Use product code (SKU) instead of product ID
        Returns:
            bool: True if successful, False if failed
        """

        try:
            if use_code:
                product = self.products.get_product_by_code(identifier, use_code=True)
                promo_id = product.get('special_offer', {}).get('promo_id')
            else:
                product = self.products.get_product_by_code(identifier)
                promo_id = product.get('special_offer', {}).get('promo_id')

            if promo_id:
                url = f'{config.SHOPER_SITE_URL}/webapi/rest/specialoffers/{promo_id}'
                response = self.client._handle_request('DELETE', url)

                if response.status_code == 200:
                    return True
                else:
                    error_description = response.json()['error_description']
                    self.outlet_logger.warning(f'❌ API Error: {error_description}')
                    self.promo_logger.warning(f'❌ API Error: {error_description}')
                    return {'success': False, 'error': error_description}
                    
        except Exception as e:
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            self.promo_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)
