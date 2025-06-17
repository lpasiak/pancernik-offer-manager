from .models.bundle_product import BundledProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.pictures import ShoperPictures
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
from tqdm import tqdm


class BundleManager:
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
                config.BUNDLE_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            return False

    def download_bundled_case_images(self):
        """Select EAN codes of a product download their images"""

        df_sku = self.gsheets_worksheets.get_data(sheet_name=config.BUNDLE_SHEET_NAME, include_row_numbers=True)
        df_sku['Case SKU'] = df_sku['SKU'].str.split('_').str[0]

        gsheets_updates = []

        number_of_products = len(df_sku)

        for index, row in tqdm(df_sku.iterrows(), total=number_of_products, desc="Processing images", unit=' image'):
            try:
                product = self.shoper_products.get_product_by_code(identifier=row['Case SKU'], use_code=True, pictures=True)

                if not product.get('img'):
                    continue
            
                google_sheets_row = row['Row Number']

                source_images = product['img']
                final_images = []
                
                for image in source_images:
                    image_id = f"{image['gfx_id']}.{image['extension']}"

                    image_item = {
                        'url': f"{config.SHOPER_SITE_URL}/userdata/public/gfx/{image_id}",
                        'main': str(image['main']),
                        'order': image['order'],
                        'name': image['translations']['pl_PL']['name']
                    }
                    final_images.append(image_item)

                final_images.sort(key=lambda x: x['order'])
                final_images = final_images[:14] # Allegro takes up to 16 images, the bundle's first 2 are taken

                image_links = ';'.join(image['url'] for image in final_images)

                if google_sheets_row is not None:
                    gsheets_updates.append([
                        google_sheets_row,
                        image_links, 
                ])
                else:
                    print(f"❌  Warning: SKU {row['Case SKU']} not found in Google Sheets!")

            except Exception as e:
                print(f'❌ Error downloading a product {product["SKU"]}: {e}')

        try:
            print("Uploading google sheets...")

            self.gsheets_worksheets.batch_update_from_a_list(
                worksheet_name=config.BUNDLE_SHEET_NAME,
                updates=gsheets_updates,
                start_column='Q',
                num_columns=1
            )
            
        except Exception as e:
            print(f'❌ Error updating')

    # def create_a_bundle(self, product_1_sku, product_2_sku):
    #     product_1 = self.shoper_products.get_product_by_code(product_1_sku, use_code=True, pictures=True)
    #     product_2 = self.shoper_products.get_product_by_code(product_2_sku, use_code=True, pictures=True)

    #     bundled_product = BundledProduct(product_1, product_2)
    #     print(bundled_product.categories)
