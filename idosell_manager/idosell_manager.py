from connections.idosell_connect import IdoSellAPIClient
from connections.idosell.products import IdoSellProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd


class IdoSellManager:
    def __init__(self):
        self.idosell_client = None
        self.gsheets_client = None
        self.idosell_products = None
        self.gsheets_worksheets = None
        
    def connect(self):
        """Initialize all necessary connections"""
        try:
            # Initialize Shoper connections
            self.idosell_client = IdoSellAPIClient(
                api_key=config.IDOSELL_API_KEY,
                site=config.IDOSELL_BIZON_B2B_SITE
            )
            self.idosell_client.connect()
            self.idosell_products = IdoSellProducts(self.idosell_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.BIZON_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            
            return True
            
        except Exception as e:
            print(f"Error initializing connections: {e}")
            return False
        
    def get_sheets_data(self):
        """"""
        selected_data = self.gsheets_worksheets.get_data(sheet_name=config.BIZON_PRODUCT_INFO, include_row_numbers=True)
        print(selected_data)
        return selected_data

    def get_idosell_product_code(self):
        """Export all the products and its identifiers: id, product_code, external_code"""
        selected_data = self.idosell_products.get_all_products()
        
        return selected_data

    def upload_product_information(self):
        """Update products with their Purchase Price, Weight and Dimensions"""
        pass
