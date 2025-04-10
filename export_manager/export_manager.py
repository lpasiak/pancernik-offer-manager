from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.pictures import ShoperPictures
from connections.shoper.categories import ShoperCategories
from connections.shopify_connect import ShopifyAPIClient
from connections.shopify.products import ShopifyProducts
from connections.easystorage_connect import EasyStorageClient
from connections.easystorage.products import EasyStorageProducts
import config
import json
import os


class ExportManagerShoper:
    def __init__(self):
        self.shoper_client = None
        self.shoper_products = None
        self.shoper_pictures = None
        
    def connect(self):
        """Initialize all necessary connections with Shoper"""
        try:
            # Initialize Shoper connections
            self.shoper_client = ShoperAPIClient(
                config.SHOPER_SITE_URL,
                config.SHOPER_LOGIN,
                config.SHOPER_PASSWORD
            )
            self.shoper_client.connect()
            self.shoper_products = ShoperProducts(self.shoper_client)
            self.shoper_pictures = ShoperPictures(self.shoper_client)
            self.shoper_categories = ShoperCategories(self.shoper_client)
            
            return True
            
        except Exception as e:
            print(f"Error initializing Shoper connections: {e}")
            return False

    def export_all_data_from_shoper(self):
        self.export_shoper_products()
        self.export_shoper_categories()

    def export_shoper_products(self):
        products = self.shoper_products.get_all_products_json()
        output_file = os.path.join(config.DRIVE_EXPORT_DIR, 'api-shoper', 'products.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
            
        print(f"Products exported successfully to {output_file}")

    def export_shoper_categories(self):
        categories = self.shoper_categories.get_all_categories_json()
        output_file = os.path.join(config.DRIVE_EXPORT_DIR, 'api-shoper', 'categories.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)
            
        print(f"Categories exported successfully to {output_file}")


class ExportManagerShopify:
    def __init__(self):
        self.shopify_client = None
        self.shoper_products = None

    def connect(self):
        """Initialize connection with Shopify"""
        try:
            self.shopify_client = ShopifyAPIClient(
                shop_url=config.SHOPIFY_CREDENTIALS['shop_url'],
                api_version=config.SHOPIFY_API_VERSION,
                api_token=config.SHOPIFY_CREDENTIALS['api_token']
            )
            self.shopify_client.connect()
            self.shopify_products = ShopifyProducts(self.shopify_client)

            return True

        except Exception as e:
            print(f"Error initializing Shopify connections: {e}")
            return False
        
    def export_shopify_products(self):
        all_products = self.shopify_products.get_all_products()
        
        with open(f'{config.DRIVE_EXPORT_DIR}/api-shopify/products.json', 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully downloaded {len(all_products)} products")

    
class ExpportManagerEasyStorage:
    def __init__(self):
        self.easystorage_client = None
        self.easystorage_products = None

    def connect(self):
        """Initialize connection with EasyStorage"""
        try:
            self.easystorage_client = EasyStorageClient(config.EASYSTORAGE_CREDENTIALS)
            self.easystorage_client.connect()
            self.easystorage_products = EasyStorageProducts(self.easystorage_client)

            return True

        except Exception as e:
            print(f"Error initializing EasyStorage connections: {e}")

    def export_wms_pancernik_products(self):
        
        try:
            products = self.easystorage_products.get_pancernik_products()

            if products is None:
                print('No products found')
                return

            output_file = os.path.join(config.DRIVE_EXPORT_DIR, 'api-easystorage', 'wms-pancernik-products.json')

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error exporting Pancernik products: {e}")

    def export_wms_bizon_products(self):

        try:
            products = self.easystorage_products.get_bizon_products()

            if products is None:
                print('No products found')
                return

            output_file = os.path.join(config.DRIVE_EXPORT_DIR, 'api-easystorage', 'wms-bizon-products.json')

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"Error exporting Bizon products: {e}")
