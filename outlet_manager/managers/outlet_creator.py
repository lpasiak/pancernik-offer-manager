from ..models.product import OutletProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.pictures import ShoperPictures
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from datetime import datetime
import config
import time

class OutletCreator:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.shoper_pictures = None
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
            self.shoper_pictures = ShoperPictures(self.shoper_client)
            
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

    def get_offers_ready_to_publish(self):
        """Get offers that are ready to be published"""
        
        df = self.gsheets_worksheets.get_data(sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True)

        if df is None:
            return None

        if 'Uszkodzenie' in df.columns:
            df['Uszkodzenie'] = df['Uszkodzenie'].str.upper()

        mask = (
            (df['Wystawione'] != 'TRUE') &
            (df['Data'].fillna('') != config.TODAY)
        )
        df = df[mask]

        df.to_excel(config.SHEETS_DIR / f'offers_ready_to_publish.xlsx', index=False)
        print(f'Selected products ready to publish: {len(df)}')

        if len(df) > 0:
            print(df[['EAN', 'SKU']])
            return df
        return None

    def create_outlet_offers(self, df_offers):
        """Create outlet offers for the given products
        Args:
            df_offers_to_be_published (df): A pandas DataFrame containing the products to create with ['EAN'] column.
        """

        if df_offers is None or df_offers.empty:
            print("No offers to create")
            return
        
        # Product counter and gsheets updates list
        date_created = datetime.today().strftime('%Y-%m-%d')
        product_count = len(df_offers)
        product_counter = 0
        gsheet_updates = []
        print(f'Creating {product_count} outlet offers')

        for _, product in df_offers.iterrows():
            source_product = self.shoper_products.get_product_by_code(product['EAN'], pictures=True, use_code=True)
            new_outlet = OutletProduct(source_product, product['SKU'], product['Uszkodzenie'])

            # Variables to be used for gsheets updates

            product_code = product['SKU']
            product_category_id = int(source_product['category_id'])

            try:

                # Get the row number of the product in the Google Sheets
                google_sheets_row = product['Row Number']

                # Create outlet offer
                product_data = new_outlet.transform_to_outlet()
                created_offer_id = self.shoper_products.create_product(product_data)
                
                # If the product is not created, skip the rest of the current iteration and move to the next product
                if created_offer_id is None:
                    print(f"❌ Failed to create outlet offer for product {product['SKU']}")
                    continue
                    
                print(f"✅ Created outlet product with ID: {created_offer_id}")
                
                # Update product details
                self.shoper_products.update_product_by_code(created_offer_id, ean=new_outlet.barcode)
                self.shoper_products.update_product_by_code(created_offer_id, related=new_outlet.related)
                
                # Update URL
                product_url = new_outlet.product_url(created_offer_id)
                product_url_json = {'pl_PL': {'seo_url': product_url}}
                product_url_link = f'{config.SHOPER_SITE_URL}/{product_url}'
                self.shoper_products.update_product_by_code(created_offer_id, translations=product_url_json)

                # Update images
                outlet_pictures = new_outlet.set_outlet_pictures(created_offer_id)
                for i, picture in enumerate(outlet_pictures, 1):
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        try:
                            self.shoper_pictures.update_product_image(created_offer_id, picture)
                            break  # Success, exit retry loop
                            
                        except Exception as e:
                            retry_count += 1
                            if retry_count == max_retries:
                                print(f"❌ Failed to upload image after {max_retries} attempts: {e}")
                            else:
                                print(f"⚠️ Image upload attempt {retry_count} failed, retrying...")
                                time.sleep(1)  # Wait before retry

                # Update stock image
                try:
                    created_product = self.shoper_products.get_product_by_code(created_offer_id)
                    if created_product and 'main_image' in created_product:
                        stock_gfx = created_product['main_image']['gfx_id']
                        self.shoper_products.update_product_by_code(created_offer_id, stock={'gfx_id': stock_gfx})
                except Exception as e:
                    print(f"Error updating stock image: {e}")

                # Creating a list of updates to be made in gsheets
                if google_sheets_row is not None:
                    gsheet_updates.append([
                        google_sheets_row,
                        True, 
                        date_created, 
                        product_url_link, 
                        int(created_offer_id), 
                        product_category_id
                    ])
                else:
                    print(f"Warning: SKU {product_code} not found in Google Sheets!")

                product_counter += 1
                print(f'Products created: {product_counter}/{product_count}')
                print('-----------------------------------')
                
            except Exception as e:
                print(f'❌ Error creating outlet offer for product {product["product_id"]}: {e}')

        print(f'Created {product_counter} outlet offers')
        # Update Google Sheets
        self.batch_update_created_offers_gsheets(gsheet_updates)

    def batch_update_created_offers_gsheets(self, gsheets_updates):
        """Save created offers to Google Sheets
        Args:
            gsheets_updates (list): List of updates containing [row_number, created, date_created, product_url, product_id, product_category_id]
        """
        try:
            self.gsheets_worksheets.batch_update_from_a_list(
                worksheet_name=config.OUTLET_SHEET_NAME,
                updates=gsheets_updates,
                start_column='F',
                num_columns=5
            )
        except Exception as e:
            print(f"Failed to update Google Sheets: {str(e)}")
