from .models.outlet_product import OutletProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
import config

shoper_client = ShoperAPIClient(
    site_url=config.SHOPER_SITE_URL,
    login=config.SHOPER_LOGIN,
    password=config.SHOPER_PASSWORD
)
shoper_client.connect()

shoper_products = ShoperProducts(shoper_client)

outlets_to_create = [
    {
        'outlet_code': 'OUT_XD1',
        'damage_type': 'USZ',
        'product_id': 86898
    },
    {
        'outlet_code': 'OUT_XD2',
        'damage_type': 'USZ',
        'product_id': 86899
    },    
    {
        'outlet_code': 'OUT_XD3',
        'damage_type': 'USZ',
        'product_id': 86900
    }
]

def display_outlets_to_create():
    for product in outlets_to_create:
        source_product = shoper_products.get_a_product_by_code(product['product_id'], pictures=True)
        new_outlet = OutletProduct(source_product, product['outlet_code'], product['damage_type'])
        print(f"✅ Product type: {new_outlet.product_type}")
        print(f"✅ Product URL: {new_outlet.product_url('xd')}")