from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
from datetime import datetime, timedelta
import pandas as pd

class OutletDiscountManager:
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
        
    def select_products_to_discount(self):
        """Get all products that have been created more than 14 days ago.
        Returns:
            A pandas DataFrame containing the products that need discounting or None if no products are found.
        """
        today = pd.Timestamp.today()

        df_all_products = self.gsheets_worksheets.get_data(sheet_name='Outlety', include_row_numbers=True)

        df_all_products['Data wystawienia'] = pd.to_datetime(
            df_all_products['Data wystawienia'], 
            format='%d-%m-%Y',
            errors='coerce'
        )
        
        # Calculate days difference
        days_difference = (today - df_all_products['Data wystawienia']).dt.days
        
        # Create mask with string comparisons for boolean columns
        mask = (
            (df_all_products['Wystawione'] == 'TRUE') & 
            (df_all_products['Druga obniżka'] == 'FALSE') &
            (days_difference >= config.OUTLET_DAYS_TO_DISCOUNT) &
            (df_all_products['Data wystawienia'].notna())  # Add check for valid dates
        )

        filtered_products = df_all_products[mask]
        
        if len(filtered_products) > 0:
            print(f'\nSelected {len(filtered_products)} products ready to discount.')
            return filtered_products
        
        return None
    
    def create_discounts(self):
        """Create discounts for products that have been in outlet for more than configured days."""
        