from outlet_manager.managers.outlet_creator import OutletCreator
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
import config

def main():
    # shoper_client = ShoperAPIClient(config.SHOPER_SITE_URL, config.SHOPER_LOGIN, config.SHOPER_PASSWORD)
    # shoper_client.connect()  # Add connect() call to authenticate
    # shoper_products = ShoperProducts(shoper_client)
    # print(shoper_products.get_a_product_by_code('8809640252648', use_code=True))


    out_creator = OutletCreator()
    out_creator.connect()
    products_to_publish = out_creator.get_offers_ready_to_publish()
    out_creator.create_outlet_offers(products_to_publish)

if __name__ == '__main__':
    main()
