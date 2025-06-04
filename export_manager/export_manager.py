from connections import ShoperAPIClient, ShopifyAPIClient, EasyStorageClient, IdoSellAPIClient
from connections.shoper import ShoperProducts, ShoperProducers, ShoperCategories
from connections.shopify.products import ShopifyProducts
from connections.easystorage.products import EasyStorageProducts
from connections.idosell.products import IdoSellProducts
import config
import json
from datetime import datetime
import shutil, os

def save_to_files(items_to_save, file):
    """Save export in project's filepath and on our drive."""
    base_file_path = f'{config.SHEETS_DIR}/api-exports/{file}.json'
    main_file_path = f'{config.DRIVE_EXPORT_DIR}/api-exports/{file}.json'
    archive_file_path = f'{config.DRIVE_EXPORT_DIR}/api-archived/{file}--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
    os.makedirs(os.path.dirname(base_file_path), exist_ok=True)

    try:
        print(f'ℹ️  Saving export to...')
        print(base_file_path)
        with open(base_file_path, 'w', encoding='utf-8') as f:
            json.dump(items_to_save, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'❌ Error saving export.')

    try:
        print(f'ℹ️  Copying export to...')
        print(main_file_path)
        shutil.copy2(base_file_path, main_file_path)
    except Exception as e:
        print(f'❌ Error copying export.')

    try:
        print(f'ℹ️  Creating a backup in...')
        print(archive_file_path)
        shutil.copy2(base_file_path, archive_file_path)
    except Exception as e:
        print(f'❌ Error copying export.')

class ExportManagerShoper:
    def __init__(self):
        self.shoper_client = None
        self.shoper_products = None
        self.shoper_categories = None
        self.shoper_producers = None
        
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
            self.shoper_categories = ShoperCategories(self.shoper_client)
            self.shoper_producers = ShoperProducers(self.shoper_client)

            return True
            
        except Exception as e:
            print(f"❌ Error initializing Shoper connections: {e}")
            return False

    def export_all_data_from_shoper(self):
        # self.export_shoper_products()
        self.export_shoper_categories()
        self.export_shoper_producers()

    def export_shoper_products(self):
        products = self.shoper_products.get_all_products_json()
        print(f"✅ Successfully downloaded {len(products)} products")
        save_to_files(items_to_save=products, file='shoper-products')

    def export_shoper_categories(self):
        categories = self.shoper_categories.get_all_categories_json()
        print(f"✅ Successfully downloaded {len(categories)} categories")
        save_to_files(items_to_save=categories, file='shoper-categories')

    def export_shoper_producers(self):
        producers = self.shoper_producers.get_all_producers_json()
        print(f"✅ Successfully downloaded {len(producers)} producers")
        save_to_files(items_to_save=producers, file='shoper-producers')

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
            print(f"❌ Error initializing Shopify connections: {e}")
            return False
        
    def export_shopify_products_light(self):
        products = self.shopify_products.get_all_products_light()
        print(f"✅ Successfully downloaded {len(products)} products")
        save_to_files(items_to_save=products, file='shopify-products_light')

    def export_shopify_products_bizon(self):
        products = self.shopify_products.get_all_products_bizon()
        print(f"✅ Successfully downloaded {len(products)} products")
        save_to_files(items_to_save=products, file='shopify-products_bizon')


class ExpportManagerEasyStorage:
    def __init__(self):
        self.easystorage_client = None
        self.easystorage_products = None

    def connect(self):
        """Initialize connection with EasyStorage"""
        try:
            self.easystorage_client = EasyStorageClient(config.DOMAIN_CREDENTIALS)
            self.easystorage_client.connect()
            self.easystorage_products = EasyStorageProducts(self.easystorage_client)

            return True

        except Exception as e:
            print(f"❌ Error initializing EasyStorage connections: {e}")

    def export_wms_pancernik_products(self):

        try:
            products = self.easystorage_products.get_pancernik_products()

            if products is None:
                print('ℹ️  No products found')
                return

            print(f"✅ Successfully downloaded {len(products)} products")
            save_to_files(items_to_save=products, file='easystorage-pancernik-products')

        except Exception as e:
            print(f"❌ Error exporting Pancernik products: {e}")

    def export_wms_bizon_products(self):

        try:
            products = self.easystorage_products.get_bizon_products()

            if products is None:
                print('ℹ️  No products found')
                return

            print(f"✅ Successfully downloaded {len(products)} products")
            save_to_files(items_to_save=products, file='easystorage-bizon-products')

        except Exception as e:
            print(f"❌ Error exporting Bizon products: {e}")

class ExportManagerIdosell:
    def __init__(self):
        self.idosell_client = None
        self.idosell_products = None
        
    def connect(self):
        """Initialize all necessary connections with IdoSell"""
        try:
            self.idosell_client = IdoSellAPIClient(
                api_key=config.IDOSELL_API_KEY,
                site=config.IDOSELL_BIZON_B2B_SITE
            )
            self.idosell_client.connect()
            self.idosell_products = IdoSellProducts(self.idosell_client)
            return True
            
        except Exception as e:
            print(f"❌ Error initializing IdoSell connections: {e}")
            return False

    def export_idosell_products_descriptions(self):

        try:
            products = self.idosell_products.get_all_products_descriptions()

            if products is None:
                print('ℹ️  No products found')
                return

            print(f"✅ Successfully downloaded {len(products)} products")
            save_to_files(items_to_save=products, file='idosell_products')

        except Exception as e:
            print(f"❌ Error exporting Bizon products: {e}")
