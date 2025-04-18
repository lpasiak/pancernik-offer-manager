from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from connections.shoper.specialoffers import ShoperSpecialOffers
import config
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
            self.shoper_special_offers = ShoperSpecialOffers(self.shoper_client)
            
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

        df = self.gsheets_worksheets.get_data(sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True)

        df['Data wystawienia'] = pd.to_datetime(
            df['Data wystawienia'], 
            format='%d-%m-%Y',
            errors='coerce'
        )

        # Calculate days difference
        days_difference = (today - df['Data wystawienia']).dt.days
        
        # Create mask with string comparisons for boolean columns
        mask = (
            (df['Wystawione'] == 'TRUE') & 
            (df['Druga obniżka'] == 'FALSE') &
            (days_difference >= config.OUTLET_DAYS_TO_DISCOUNT) &
            (df['Data wystawienia'].notna())  # Add check for valid dates
        )

        df = df[mask]
        
        if len(df) > 0:
            print(f'ℹ️ Selected {len(df)} products ready to discount.')
            return df
        return None
    
    def create_discounts(self, df_offers_to_discount):
        """Create discounts for products that have been in outlet for more than configured days.
        Note: If there is an existent discounts, it removes it and creates a new one.
        Args:
            df_offers_to_discount (df): A pandas DataFrame containing the products to create with ['EAN'] column.
        """
        
        if df_offers_to_discount is None or df_offers_to_discount.empty:
            print("No offers to discount")
            return
        
        # Testing on 2 products
        # df_offers_to_discount = df_offers_to_discount.head(2)
        
        product_discount_count = len(df_offers_to_discount)
        product_discount_counter = 0
        gsheets_updates = []
        print(f'Discounting {product_discount_count} outlet offers')
        
        for _, product in df_offers_to_discount.iterrows():

            try:
                # Get the row number of the product in the Google Sheets
                google_sheets_row = product['Row Number']
                product_code = product['SKU']
                product_id = product['ID Shoper']

                # Create a special offer
                product_data = {
                    'product_id': product_id,
                    'discount': config.OUTLET_DISCOUNT_PERCENTAGE,
                    'discount_type': 3
                }
                
                # TODO: Temporary solution. Come back to it and remove reduntant api calls.
                product_info = self.shoper_products.get_product_by_code(product_id)
                if product_info and product_info.get('special_offer'):
                    self.shoper_special_offers.remove_special_offer_from_product(product_id)

                # Create a new special offer
                self.shoper_special_offers.create_special_offer(product_data)

                # Creating a list of updates to be made in gsheets
                if google_sheets_row is not None:
                    gsheets_updates.append([
                        google_sheets_row,
                        True
                    ])
                else:
                    print(f"Warning: SKU {product_code} not found in Google Sheets!")

                product_discount_counter += 1
                print(f'Set {config.OUTLET_DISCOUNT_PERCENTAGE}% discount for {product_code}')
                print(f'Products discounted: {product_discount_counter}/{product_discount_count}')
                print('-----------------------------------')

            except Exception as e:
                print(f'❌ Error creating special offer {product_code}: {e}')
                continue

        print(f"Updating Google Sheets for {len(gsheets_updates)} products...")
        if gsheets_updates:
            self.batch_update_discounted_offers_gsheets(gsheets_updates)
        
    def batch_update_discounted_offers_gsheets(self, gsheets_updates):
        """Save discounted offers' info to Google Sheets
        Args:
            gsheets_updates (list): List of updates containing [row_number, discount]
        """
        try:
            self.gsheets_worksheets.batch_update_from_a_list(
                worksheet_name=config.OUTLET_SHEET_NAME,
                updates=gsheets_updates,
                start_column='K',
                num_columns=1
            )
            print("✅ Successfully updated Google Sheets")
        except Exception as e:
            print(f"❌ Failed to update Google Sheets: {str(e)}")
