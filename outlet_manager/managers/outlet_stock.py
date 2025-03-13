from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
from datetime import datetime

class OutletStockManager:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.gsheets_worksheets = None
        
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
            
            return True
            
        except Exception as e:
            print(f"Error initializing connections: {e}")
            return False
        
    def move_products_to_lacking(self):
        """Move products that have no offers on shoper to the lacking gsheet"""
        today = datetime.today().strftime('%d-%m-%Y')

        # datetime.today().strftime('%Y-%m-%d')
        # Get all products from the outlet gsheet
        df_all_products = self.gsheets_worksheets.get_data(sheet_name='Outlety', include_row_numbers=True)

        mask = (
            (df_all_products["Wystawione"] != 'TRUE') & 
            (df_all_products['Data'].fillna('') != today))

        columns_to_keep = ['Row Number', 'EAN', 'SKU', 'Nazwa', 'Uszkodzenie', 'Data']
        df_all_products = df_all_products[columns_to_keep]

        selected_offers = df_all_products[mask].copy()

        print('\nℹ️ Checking if all the products exist on Shoper...\n')
        
        # If there are no products to move, return
        if selected_offers.empty:
            print('\nℹ️ No products to move to the lacking sheet\n')
            return

        # Check if the products exist on Shoper
        for index, row in selected_offers.iterrows():
            response = self.shoper_products.get_product_by_code(row['EAN'], use_code=True)
            
            if response is not None:
                selected_offers = selected_offers.drop(index)
                print(f'ℹ️ Product {row["EAN"]} exists on Shoper.')

        if selected_offers.empty:
            print('ℹ️ No products to move to the lacking sheet')
            return

        selected_offers = selected_offers[columns_to_keep]

        # Move products to the lacking gsheet and remove them from the outlet gsheet
        self.gsheets_worksheets.batch_move_products(
            source_worksheet_name=config.OUTLET_SHEET_NAME,
            target_worksheet_name=config.OUTLET_SHEET_LACKING_PRODUCTS_NAME,
            values_df=selected_offers
        )

        print('✅ Products moved to the lacking sheet')
