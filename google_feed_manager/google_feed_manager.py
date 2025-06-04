
from connections import ShoperAPIClient, GSheetsClient, SubiektClient
from connections.shoper.products import ShoperProducts
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd
import json


class GoogleCostOfGoodsSold:
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
                config.PRICES_SHEET_FOR_COGS_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            return False
        
    def _convert_json_to_df(self, filepath):
        """Convert JSON file to DataFrame
        Args:
            filepath (str): Path to the JSON file
        Returns:
            pd.DataFrame: DataFrame with selected columns
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data_list = list(data.values())

            return pd.DataFrame(data_list)

    def get_all_products_from_shoper(self):
        df_products = self._convert_json_to_df(config.SHEETS_DIR / 'api-exports' / 'shoper-beautiful-products.json')
        return df_products

    def get_prices_bizon(self):
        self.gsheets_worksheets.get_data('Bizon')
