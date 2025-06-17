import config
import random
from PIL import Image


class BundledProduct:
    """
    BundledProduct is a Class that transforms 2 regular products into a product that is a bundled product.
    Args:
        product_data (dict): The product data from the Shoper API.
        outlet_code (str): The outlet code.
        damage_type (str): The damage type one of the ['USZ', 'ZAR', 'OBA']
    """
    def __init__(self, product_1, product_2):
        self.code = f'{product_1['code']}_{product_2['code']}'
        self.producer_id = product_1['producer_id']
        self.category_id = product_1['category_id']
        self.categories = list(set(product_1['categories'] + product_2['categories']))
        self.pkwiu = product_1['pkwiu']
        self.stock = {
            'stock': 999,
            'price': float(product_1['stock']['price']) + float(product_2['stock']['price']),
            'active': 1,
            'availability_id': None,
            'delivery_id': 1,
            'weight': 0.2,
            'weight_type': product_1['weight_type']
        }
        self.translations = {
            'pl_PL': {
                'name': 'Testowy zestaw Bizon',
                'short_description': '',
                'description': '',
                'active': '1',
                'order': random.randint(5,15)
            }
        }
        self.type = 1
        self.newproduct = 0
        self.related = product_1['related']

    def transform_to_bundle(self):
        bundle_product = {
            'producer_id': self.producer_id,
            'category_id': self.category_id,
            'categories': self.categories,
            'additional_producer': '',
            'code': self.code,
            'pkwiu': self.pkwiu,
            'stock': self.stock,
            'translations': self.translations,
            'type': self.type,
            'newproduct': 0,
            'related': self.related
        }

        return bundle_product
        
    def _generate_product_name(self):
        pass

    def _generate_product_short_description(self):
        pass

    def _generate_product_description(self):
        description_1 = self.product_1['translations']['pl_PL']['description'].replace('</hr>', '<hr>')
        description_2 = self.product_2['translations']['pl_PL']['description'].replace('</hr>', '<hr>')

    def _create_main_picture(self):
        pass