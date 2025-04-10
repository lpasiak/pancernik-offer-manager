from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from connections.easystorage_connect import EasyStorageClient
import config
import pandas as pd


class OutletArchiver:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.gsheets_worksheets = None
        self.easystorage_data = None
        
    def connect(self):
        """Initialize all necessary connections"""
        try:
            # Initialize Shoper connections
            self.shoper_client = ShoperAPIClient(
                config.SHOPER_SITE_URL,
                config.SHOPER_LOGIN,
                config.SHOPER_PASSWORD
            )
            self.shoper_client.connect()
            self.shoper_products = ShoperProducts(self.shoper_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.OUTLET_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            self.easystorage_file = EasyStorageClient(config.EASYSTORAGE_FILE_PATH)
            self.easystorate_data = self.easystorage_file.outlet_products
            
            return True
            
        except Exception as e:
            print(f"Error initializing connections: {e}")
            return False
        
    def select_sold_products(self):
        """Move products that have been sold
        Returns:
            A pandas DataFrame containing the products that were sold
        """

        try:
            easy_storage_data = self.easystorate_data
            easy_storage_sku_list = easy_storage_data['SKU'].tolist()
            gsheets_data = self.gsheets_worksheets.get_data(sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True)

            mask = (
                (gsheets_data['Wystawione'] == 'TRUE') &
                (gsheets_data['ID Shoper'].notna()) &
                (gsheets_data['ID Shoper'] != '') &
                (gsheets_data['ID Shoper'] != 0)
            )

            if gsheets_data.empty:
                return

            columns_to_keep = ['Row Number', 'EAN', 'SKU', 'Nazwa', 'Uszkodzenie', 'Data', 'Wystawione', 'Data wystawienia', 'Druga obniżka', 'ID Shoper']

            gsheets_data = gsheets_data[mask]
            gsheets_data = gsheets_data[columns_to_keep]

            gsheets_length = len(gsheets_data)

            print(f'{gsheets_length} products to analyze...')
            for index, row in gsheets_data.iterrows():

                try:
                    product_sku = row['SKU']
                    product_data = self.shoper_products.get_product_by_code(row['ID Shoper'])
                    product_stock = int(product_data['stock']['stock'])

                    print(f'Analyzing product {product_sku} | {index + 1}/{gsheets_length}')
                    
                    # If product has 0 items on Shoper and it is not in easy storage warehouse
                    if product_stock != 0 or product_sku in easy_storage_sku_list:
                        gsheets_data = gsheets_data.drop(index)
                except Exception as e:
                    print(f"Error: {e}")
                    gsheets_data = gsheets_data.drop(index)
                    continue

            if gsheets_data.empty:
                print('No products sold.')
                return
            
            print(f'{len(gsheets_data)} Products that were sold:')
            print(gsheets_data[['SKU', 'Nazwa']])
            return gsheets_data
        
        except Exception as e:
            print(f"Error selecting products to be cleaned: {e}")
        
    def archive_sold_products(self, sold_products_df):

        if sold_products_df is None or (isinstance(sold_products_df, pd.DataFrame) and sold_products_df.empty):
            return
        
        # Add necessary columns and format them (so it uploads correctly to Google Sheets)
        sold_products_df['Status'] = 'Sprzedane'
        sold_products_df['Zutylizowane'] = True
        sold_products_df['Wystawione'] = True
        sold_products_df['Druga obniżka'] = sold_products_df['Druga obniżka'].map({'TRUE': True, 'FALSE': False})
        sold_products_df['SKU'] = sold_products_df['SKU'].astype('object')

        sold_products_df = sold_products_df.replace({float('nan'): None, 'nan': None})

        sold_products_len = len(sold_products_df)
        counter = 0

        # Remove from Shoper
        for index, row in sold_products_df.iterrows():
            self.shoper_products.remove_product(row['ID Shoper'])
            counter += 1
            print(f'Products: {counter}/{sold_products_len}')

        # Move to archived sheet
        offers_to_move = sold_products_df[['Row Number', 'EAN', 'SKU', 'Nazwa', 'Uszkodzenie', 'Data', 'Wystawione', 'Data wystawienia', 'Druga obniżka', 'Status', 'Zutylizowane']]
        self.gsheets_worksheets.batch_move_products(
            source_worksheet_name=config.OUTLET_SHEET_NAME,
            target_worksheet_name=config.OUTLET_SHEET_ARCHIVED_NAME,
            values_df=offers_to_move
        )
        
