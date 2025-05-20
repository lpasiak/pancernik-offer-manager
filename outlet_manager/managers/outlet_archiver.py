from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.orders import ShoperOrders
from connections.shoper.redirects import ShoperRedirects
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from connections.easystorage_connect import EasyStorageClient
from connections.easystorage.products import EasyStorageProducts
import config
import pandas as pd
from datetime import datetime
from tqdm import tqdm
from utils.logger import get_outlet_logger


class OutletArchiver:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.easystorage_client = None
        self.shoper_products = None
        self.shoper_orders = None
        self.shoper_redirects = None
        self.gsheets_worksheets = None
        self.easystorage_products = None
        self.outlet_logger = get_outlet_logger().get_logger()

    def connect(self):
        """Initialize all necessary connections"""
        try:
            # Initialize Shoper connection
            self.shoper_client = ShoperAPIClient(
                config.SHOPER_SITE_URL,
                config.SHOPER_LOGIN,
                config.SHOPER_PASSWORD
            )
            self.shoper_client.connect()
            self.shoper_products = ShoperProducts(self.shoper_client)
            self.shoper_redirects = ShoperRedirects(self.shoper_client)
            self.shoper_orders = ShoperOrders(self.shoper_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.OUTLET_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)

            # Initialize EasyStorage connection
            self.easystorage_client = EasyStorageClient(config.EASYSTORAGE_CREDENTIALS)
            self.easystorage_client.connect()
            self.easystorage_products = EasyStorageProducts(self.easystorage_client)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            self.outlet_logger.warning(f"❌ Error initializing connections: {e}")
            return False

    def _generate_ready_df(self, gsheets_data, products, type):
        rows_to_drop = [idx for idx in gsheets_data.index if idx not in products]
        products_df = gsheets_data.drop(rows_to_drop).copy()

        if type == 'archive':
            products_df['URL'] = [products[idx]['URL'] for idx in products_df.index]

        print(f'ℹ️  Products to {type}: {len(products_df)}')
        self.outlet_logger.info(f'ℹ️ Products to {type}: {len(products_df)}')
        products_df.to_excel(config.SHEETS_DIR / f'products_to_{type}.xlsx', index=False)

        return products_df
            
    def categorize_products(self):
        """Determine which products are sold and should be archived. Show products that should be activated back on Shoper."""
        try:
            # Get EasyStorage outlet products with non-zero stock
            easy_storage_products = self.easystorage_products.get_pancernik_products()
            easy_storage_sku_list = {
                product['sku']
                for product in easy_storage_products
                if 'OUT' in product.get('sku', '').upper() and product.get('available_quantity', 0) != 0
            }

            # Get latest order products from Shoper (to check if they were sold lately)
            bought_products_json = self.shoper_orders.get_latest_order_products(pages_to_fetch=200)
            bought_products_list = list(set([product['code'] for product in bought_products_json]))

            # Download GSheets product data
            gsheets_data = self.gsheets_worksheets.get_data(
                sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True
            )

            # Filter rows with valid IDs and published status
            mask = (
                (gsheets_data['Wystawione'] == 'TRUE') &
                (gsheets_data['ID Shoper'].notna()) &
                (gsheets_data['ID Shoper'] != '') &
                (gsheets_data['ID Shoper'] != 0)
            )
            columns_to_keep = [
                'Row Number', 'EAN', 'SKU', 'Nazwa', 'Uszkodzenie', 'Data',
                'Wystawione', 'Data wystawienia', 'Druga obniżka', 'ID Shoper'
            ]
            gsheets_data = gsheets_data.loc[mask, columns_to_keep].copy()

            # Track products to archive and their URLs
            products_to_archive = {}
            products_to_activate = {}
            products_to_deactivate = {}

            for index, row in tqdm(gsheets_data.iterrows(), total=len(gsheets_data), desc="Analyzing products", unit=" product"):
                try:
                    product_sku = row['SKU']
                    product_data = self.shoper_products.get_product_by_code(row['ID Shoper'])
                    product_stock = int(product_data['stock']['stock'])

                    # All the options:
                    # 1. Product was sold - 0 on Shoper, 0 in EasyStorage - TO BE REMOVED
                    # 2. Product was not sold - 0 on Shoper, 1 in EasyStorage and not bought recently - TO BE ACTIVATED
                    # 3. Product was probably sold - 0 on Shoper, 1 in EasyStorage and bought recently - TO BE 0 stock 0 active

                    if product_stock == 0 and product_sku not in easy_storage_sku_list:
                        products_to_archive[index] = {
                            'URL': product_data['translations']['pl_PL'].get('seo_url', ''),
                            'sku': product_sku
                        }
                    elif product_stock == 0 and product_sku in easy_storage_sku_list and product_sku not in bought_products_list:
                        products_to_activate[index] = {
                            'sku': product_sku
                        }
                    elif product_stock == 0 and product_sku in easy_storage_sku_list and product_sku in bought_products_list:
                        products_to_deactivate[index] = {
                            'sku': product_sku
                        }

                except Exception as e:
                    print(f"❌ Error for SKU {row['SKU']}: {e}")
                    self.outlet_logger.warning(f"❌ Error for SKU {row['SKU']}: {e}")
            
            # Generate DataFrames for each product category
            products_to_archive_df = self._generate_ready_df(gsheets_data, products_to_archive, 'archive')
            products_to_activate_df = self._generate_ready_df(gsheets_data, products_to_activate, 'activate')
            products_to_deactivate_df = self._generate_ready_df(gsheets_data, products_to_deactivate, 'deactivate')

            return products_to_archive_df, products_to_activate_df, products_to_deactivate_df

        except Exception as e:
            print(f"❌ Error selecting products to be cleaned: {e}")
            self.outlet_logger.warning(f"❌ Error selecting products to be cleaned: {e}")
            return None, None, None

    def archive_sold_products(self, sold_products_df):
            
        date_removed = datetime.today().strftime('%Y-%m-%d')

        if sold_products_df is None or (isinstance(sold_products_df, pd.DataFrame) and sold_products_df.empty):
            self.outlet_logger.info(f'❌ Nothing to archive.')
            return
        
        try:
 
            # Add necessary columns and format them (so it uploads correctly to Google Sheets)
            sold_products_df['Status'] = 'Sprzedane'
            sold_products_df['Zutylizowane'] = True
            sold_products_df['Wystawione'] = True
            sold_products_df['Druga obniżka'] = sold_products_df['Druga obniżka'].map({'TRUE': True, 'FALSE': False})
            sold_products_df['SKU'] = sold_products_df['SKU'].astype('object')
            sold_products_df['Data usunięcia'] = date_removed
            sold_products_df['Komentarz'] = ''
            sold_products_df = sold_products_df.replace({float('nan'): None, 'nan': None})

            sold_products_len = len(sold_products_df)
            counter = 0

            # Remove from Shoper and create a redirection
            for index, row in sold_products_df.iterrows():
                self.shoper_products.remove_product(row['ID Shoper'])

                redirect_data = {
                'redirected_url': row['URL'],
                'target_url': config.REDIRECT_TARGET_OUTLET_URL
                }

                redirect_id = self.shoper_redirects.create_redirect(redirect_data)
                sold_products_df.at[index, 'ID Przekierowania'] = redirect_id

                counter += 1
                print(f'Products: {counter}/{sold_products_len}')

            # Move to archived sheet
            offers_to_move = sold_products_df[[
                'Row Number',
                'EAN',
                'SKU', 
                'Nazwa',
                'Uszkodzenie',
                'Data',
                'Wystawione',
                'Data wystawienia',
                'Druga obniżka',
                'Status',
                'Zutylizowane',
                'Komentarz',
                'Data usunięcia',
                'URL',
                'ID Przekierowania'
            ]]

            self.gsheets_worksheets.batch_move_products(
                source_worksheet_name=config.OUTLET_SHEET_NAME,
                target_worksheet_name=config.OUTLET_SHEET_ARCHIVED_NAME,
                values_df=offers_to_move
            )

            return sold_products_len
        
        except Exception as e:
            print(f'❌ Error archiving products: {e}')
            self.outlet_logger.warning(f'❌ Error archiving products: {e}')
            return 0
    
    def reactivate_products(self, products_to_activate_df):
        """Reactivate products on Shoper"""
        try:

            if products_to_activate_df is None or products_to_activate_df.empty:
                return 0
            
            for _, row in products_to_activate_df.iterrows():
                self.shoper_products.update_product_by_code(row['ID Shoper'], stock={'stock': 1}, translations={'pl_PL': {'active': 1}})

            return len(products_to_activate_df)
                    
        except Exception as e:
            print(f"❌ Error reactivating products: {e}")
            self.outlet_logger.warning(f"❌ Error reactivating products: {e}")
            return 0

    def deactivate_products(self, products_to_deactivate_df):
        """Deactivate products on Shoper"""
        try:
            if products_to_deactivate_df is None or products_to_deactivate_df.empty:
                return 0
            
            for _, row in products_to_deactivate_df.iterrows():
                self.shoper_products.update_product_by_code(row['ID Shoper'], stock={'stock': 0}, translations={'pl_PL': {'active': 0}})

            return len(products_to_deactivate_df)

        except Exception as e:
            print(f"❌ Error deactivating products: {e}")
            self.outlet_logger.warning(f"❌ Error deactivating products: {e}")
            return 0

