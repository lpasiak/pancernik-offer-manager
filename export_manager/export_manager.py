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
from datetime import datetime
import shutil, os


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
        print(f"Successfully downloaded {len(products)} products")

        # Save to the main file
        file = f'{config.SHEETS_DIR}/api-exports/shoper-products.json'
        os.makedirs(os.path.dirname(file), exist_ok=True)

        print(f'Saving export to {file}...')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)

        # Copy and save to the main file
        main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/shoper-products.json'
        print(f'Copying export to {main_file}...')
        shutil.copy2(file, main_file)    
            
        # Copy and save to the archived with timestamp
        archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/shoper-products--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
        print(f'Copying export to {archive_file}...')
        shutil.copy2(main_file, archive_file)        


    def export_shoper_categories(self):
        categories = self.shoper_categories.get_all_categories_json()
        print(f"Successfully downloaded {len(categories)} categories")

        # Save to the main file
        file = f'{config.SHEETS_DIR}/api-exports/shoper-categories.json'
        os.makedirs(os.path.dirname(file), exist_ok=True)

        print(f'Saving export to {file}...')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=4)

        # Copy and save to the main file
        main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/shoper-categories.json'
        print(f'Copying export to {main_file}...')
        shutil.copy2(file, main_file)
            
        # Copy and save to the archived with timestamp
        archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/shoper-categories--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
        print(f'Copying export to {archive_file}...')
        shutil.copy2(main_file, archive_file)


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
        
    def export_shopify_products_light(self):
        all_products = self.shopify_products.get_all_products_light()
        print(f"Successfully downloaded {len(all_products)} products")

        # Save to the main file
        file = f'{config.SHEETS_DIR}/api-exports/shopify-products-light.json'
        os.makedirs(os.path.dirname(file), exist_ok=True)

        print(f'Saving export to {file}...')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)

        # Copy and save to the main file
        main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/shopify-products-light.json'
        print(f'Copying export to {main_file}...')
        shutil.copy2(file, main_file)
            
        # Copy and save to the archived with timestamp
        archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/shopify-products-light--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
        print(f'Copying export to {archive_file}...')
        shutil.copy2(main_file, archive_file)

    def export_shopify_products_bizon(self):
        all_products = self.shopify_products.get_all_products_bizon()
        print(f"Successfully downloaded {len(all_products)} products")

        # Save to the main file
        file = f'{config.SHEETS_DIR}/api-exports/shopify-products-bizon.json'
        os.makedirs(os.path.dirname(file), exist_ok=True)
        
        print(f'Saving export to {file}...')
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=4)

        # Copy and save to the main file
        main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/shopify-products-bizon.json'
        print(f'Copying export to {main_file}...')
        shutil.copy2(file, main_file)
            
        # Copy and save to the archived with timestamp
        archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/shopify-products-bizon--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
        print(f'Copying export to {archive_file}...')
        shutil.copy2(main_file, archive_file)


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

            print(f"Successfully downloaded {len(products)} products")

            # Save to the main file
            file = f'{config.SHEETS_DIR}/api-exports/easystorage-pancernik-products.json'
            os.makedirs(os.path.dirname(file), exist_ok=True)
            print(f'Saving export to {file}...')
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)

            # Copy and save to the main file
            main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/easystorage-pancernik-products.json'
            print(f'Copying export to {main_file}...')
            shutil.copy2(file, main_file)    

            # Copy and save to the archived with timestamp
            archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/easystorage-pancernik-products--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
            print(f'Copying export to {archive_file}...')
            shutil.copy2(main_file, archive_file)

        except Exception as e:
            print(f"Error exporting Pancernik products: {e}")

    def export_wms_bizon_products(self):

        try:
            products = self.easystorage_products.get_bizon_products()

            if products is None:
                print('No products found')
                return

            print(f"Successfully downloaded {len(products)} products")

            # Save to the main file
            file = f'{config.SHEETS_DIR}/api-exports/easystorage-bizon-products.json'
            os.makedirs(os.path.dirname(file), exist_ok=True)
            print(f'Saving export to {file}...')
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(products, f, ensure_ascii=False, indent=4)

            # Copy and save to the main file
            main_file = f'{config.DRIVE_EXPORT_DIR}/api-exports/easystorage-bizon-products.json'
            print(f'Copying export to {main_file}...')
            shutil.copy2(file, main_file)    

            # Copy and save to the archived with timestamp
            archive_file = f'{config.DRIVE_EXPORT_DIR}/api-archived/easystorage-bizon-products--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.json'
            print(f'Copying export to {archive_file}...')
            shutil.copy2(main_file, archive_file)

        except Exception as e:
            print(f"Error exporting Bizon products: {e}")
