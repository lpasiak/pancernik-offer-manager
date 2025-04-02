import config
import random


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
        self.pkwiu = product_1['pkwiu']
        self.stock = {
            'stock': 999,
            'price': float(product_1['stock']['price']) + float(product_2['stock']['price'])
        }
        self.translations = {
            'pl_PL': {
                'name': 'Testowy zestaw Bizon',
                'description': f'Zestaw {product_1['translations']['pl_PL']['description']} i {product_2['translations']['pl_PL']['description']}',
                'active': '1',
                'order': random.randint(1,5)
            }
        }
        self.type = 1

    def transform_to_bundle(self):
        bundle_product = {
            'producer_id': self.producer_id,
            'category_id': self.category_id,
            'code': self.code,
            'pkwiu': self.pkwiu,
            'stock': self.stock,
            'translations': self.translations,
            'type': self.type,
            'newproduct': 0
        }

        return bundle_product
