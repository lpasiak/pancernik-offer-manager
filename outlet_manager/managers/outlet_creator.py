from ..models.outlet_product import OutletProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.pictures import ShoperPictures
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from utils.logger import get_outlet_logger
from datetime import datetime
import pandas as pd
import config
import time
from tqdm import tqdm


class OutletCreator:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.shoper_pictures = None
        self.gsheets_worksheets = None
        self.outlet_logger = get_outlet_logger().get_logger()
        
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
            print(f'❌ Error initializing connections: {e}')
            self.outlet_logger.critical('❌ Error initializing connections: {e}')
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
            (df['Data'].fillna('') != config.TODAY) &
            (pd.to_datetime(df['Data'].fillna(''), format='%d-%m-%Y', errors='coerce').notna()) &
            (df['Data'].fillna('').str.len() > 0)
        )

        df = df[mask]

        self.outlet_logger.info(f'ℹ️ Selected products ready to publish: {len(df)}')

        if len(df) > 0:
            return df
        return None

    def create_outlet_offers(self):
        """Create outlet offers for the given products
        Returns:
            number of created offers (int)
        """
        df_offers = self.get_offers_ready_to_publish()

        if df_offers is None or df_offers.empty:
            return
        
        # Product counter and gsheets updates list
        date_created = datetime.today().strftime('%Y-%m-%d')
        product_count = len(df_offers)
        product_counter = 0
        gsheet_updates = []

        for _, product in tqdm(df_offers.iterrows(), total=product_count, desc="Creating outlet offers", unit=" offer"):

            try:

                source_product = self.shoper_products.get_product_by_code(product['EAN'], pictures=True, use_code=True)
                new_outlet = OutletProduct(source_product, product['SKU'], product['Uszkodzenie'])

                product_code = product['SKU']
                product_category_id = int(source_product['category_id'])
                
                # Get the row number of the product in the Google Sheets
                google_sheets_row = product['Row Number']

                # Create outlet offer
                product_data = new_outlet.transform_to_outlet()
                created_offer_id = self.shoper_products.create_product(product_data)
                
                # If the product is not created, skip the rest of the current iteration and move to the next product
                if created_offer_id is None:
                    self.outlet_logger.warning(f'❌ Failed to create outlet offer for product {product['SKU']} | {product['EAN']}')
                    continue
                    
                product_counter += 1

                self.outlet_logger.info(f'✅ Created outlet product with ID: {created_offer_id} | {product['SKU']} | {product['EAN']}')
                
                # Update product details
                response_barcode = self.shoper_products.update_product_by_code(created_offer_id, ean=new_outlet.barcode)

                if response_barcode == True:
                    self.outlet_logger.info(f'✅ Updated product barcode with {new_outlet.barcode}')
                else:
                    self.outlet_logger.warning(f'❌ Failed to update product barcode with {new_outlet.barcode}')

                response_related = self.shoper_products.update_product_by_code(created_offer_id, related=new_outlet.related)

                if response_related == True:
                    self.outlet_logger.info(f'✅ Updated product related')
                else:
                    self.outlet_logger.warning(f'❌ Failed to update product barcode with {new_outlet.related}')
                    
                # Update URL
                product_url = new_outlet.product_url(created_offer_id)
                product_url_json = {'pl_PL': {'seo_url': product_url}}
                product_url_link = f'{config.SHOPER_SITE_URL}/{product_url}'

                response_url = self.shoper_products.update_product_by_code(created_offer_id, translations=product_url_json)

                if response_url == True:
                    self.outlet_logger.info(f'✅ Updated product url')
                else:
                    self.outlet_logger.warning(f'❌ Failed to update product url with {product_url_json}')

                # Update images
                outlet_pictures = new_outlet.set_outlet_pictures(created_offer_id)
                images_uploaded = 0

                for i, picture in enumerate(outlet_pictures, 1):
                    max_retries = 3
                    retry_count = 0
                    
                    while retry_count < max_retries:
                        try:
                            response = self.shoper_pictures.update_product_image(picture)

                            if response.status_code == 200:
                                images_uploaded = images_uploaded + 1
                                break  # Success, exit retry loop
                            
                        except Exception as e:
                            retry_count += 1
                            if retry_count == max_retries:
                                self.outlet_logger.warning(f'❌ Failed to upload image after {max_retries} attempts: {e}')
                            else:
                                time.sleep(1)  # Wait before retry

                if images_uploaded > 0:
                    self.outlet_logger.info(f'✅ Updated {images_uploaded} images')

                # Update stock image
                try:
                    created_product = self.shoper_products.get_product_by_code(created_offer_id)
                    if created_product and 'main_image' in created_product:
                        stock_gfx = created_product['main_image']['gfx_id']
                        response = self.shoper_products.update_product_by_code(created_offer_id, stock={'gfx_id': stock_gfx})

                        if response == True:
                            self.outlet_logger.info(f'✅ Updated product main image')

                except Exception as e:
                    self.outlet_logger.warning(f'❌ Error updating stock image: {e}')

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
                    self.outlet_logger.warning(f'❌ SKU {product_code} not found in Google Sheets!')
                
            except Exception as e:
                self.outlet_logger.critical(f'❌ Error creating outlet offer for product {product["SKU"]}')

        self.outlet_logger.info(f'ℹ️ Offers created: {product_counter}/{product_count}')

        # Update Google Sheets
        self.batch_update_created_offers_gsheets(gsheet_updates)

        return product_counter


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
            self.outlet_logger.critical(f'❌ Failed to update Google Sheets: {str(e)}')
