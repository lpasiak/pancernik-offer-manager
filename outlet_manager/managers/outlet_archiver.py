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

    def select_sold_products(self):
        """Move products that have been sold.
        Returns:
            A pandas DataFrame containing the products that were sold.
        """
        try:
            # Get EasyStorage outlet products with non-zero stock
            easy_storage_products = self.easystorage_products.get_pancernik_products()
            easy_storage_sku_list = {
                product['sku']
                for product in easy_storage_products
                if 'OUT' in product.get('sku', '').upper() and product.get('stock_quantity', 0) != 0
            }

            # Download GSheets product data
            gsheets_data = self.gsheets_worksheets.get_data(
                sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True
            )

            if gsheets_data.empty:
                print('Google Sheet is empty.')
                return

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

            # Track rows to drop and URLs to update
            rows_to_drop = []
            urls_to_update = {}

            for index, row in tqdm(gsheets_data.iterrows(), total=len(gsheets_data), desc="Analyzing products", unit="product"):
                try:
                    product_sku = row['SKU']
                    product_data = self.shoper_products.get_product_by_code(row['ID Shoper'])
                    product_stock = int(product_data['stock']['stock'])

                    if product_stock != 0 or product_sku in easy_storage_sku_list:
                        rows_to_drop.append(index)
                    else:
                        urls_to_update[index] = product_data['translations']['pl_PL'].get('seo_url', '')

                except Exception as e:
                    print(f"❌ Error for SKU {row['SKU']}: {e}")
                    self.outlet_logger.warning(f"❌ Error for SKU {row['SKU']}: {e}")
                    rows_to_drop.append(index)

            # Apply changes
            gsheets_data.drop(index=rows_to_drop, inplace=True)
            for index, url in urls_to_update.items():
                gsheets_data.at[index, 'URL'] = url

            if gsheets_data.empty:
                print('No products sold.')
                return

            print(f'ℹ️  Products identified as sold: {len(gsheets_data)}')
            return gsheets_data

        except Exception as e:
            print(f"❌ Error selecting products to be cleaned: {e}")
            self.outlet_logger.warning(f"❌ Error selecting products to be cleaned: {e}")

    def archive_sold_products(self, sold_products_df):

        date_removed = datetime.today().strftime('%Y-%m-%d')

        if sold_products_df is None or (isinstance(sold_products_df, pd.DataFrame) and sold_products_df.empty):
            return
        
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