from .models.outlet_product import OutletProduct
from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts, ShoperPictures
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
from typing import Optional
import pandas as pd

class OutletManager:
    def __init__(self):
        self.shoper_client: Optional[ShoperAPIClient] = None
        self.gsheets_client: Optional[GSheetsClient] = None
        self.shoper_products: Optional[ShoperProducts] = None
        self.shoper_pictures: Optional[ShoperPictures] = None
        self.gsheets_worksheets: Optional[GsheetsWorksheets] = None
        
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
        
        assert self.gsheets_worksheets is not None  # Tell linter this won't be None
        df = self.gsheets_worksheets.get_data(sheet_name='Outlety', include_row_numbers=True)

        if df is None:
            return None

        if 'Uszkodzenie' in df.columns:
            df['Uszkodzenie'] = df['Uszkodzenie'].str.upper()

        mask = (
            (df['Wystawione'] != 'TRUE') &
            (df['Data'].fillna('') != config.TODAY)
        )
        df = df[mask]

        df.to_excel(config.SHEETS_DIR / f'offers_ready_to_publish {config.TODAY}.xlsx', index=False)
        print(f'Selected products ready to publish: {len(df)}')

        if len(df) > 0:
            print(df)
            return df
        return None

    def create_outlet_offers(self, df_offers_to_be_published):
        """Create outlet offers for the given products
        Args:
            df_offers_to_be_published (df): A pandas DataFrame containing the products to create with ['EAN'] column.
        """
        assert self.shoper_products is not None  # Tell linter this won't be None
        assert self.shoper_pictures is not None  # Tell linter this won't be None
        assert self.shoper_client is not None  # Tell linter this won't be None

        if df_offers_to_be_published is None or df_offers_to_be_published.empty:
            print("No offers to create")
            return

        for _, product in df_offers_to_be_published.iterrows():
            source_product = self.shoper_products.get_a_product_by_code(product['EAN'], pictures=True, use_code=True)
            new_outlet = OutletProduct(source_product, product['SKU'], product['Uszkodzenie'])

            try:
                # Create and update outlet offer
                self._update_outlet_after_creation(new_outlet)
                print('-----------------------------------')
                
            except Exception as e:
                print(f'❌ Error creating outlet offer for product {product["product_id"]}: {e}')

    def _update_outlet_after_creation(self, new_outlet):
        """Helper function to update an outlet offer after it gets created"""
        assert self.shoper_products is not None  # Tell linter this won't be None
        assert self.shoper_pictures is not None  # Tell linter this won't be None
        
        product_data = new_outlet.transform_to_outlet()
        created_offer_id = self.shoper_products.create_product(product_data)
        
        if not created_offer_id:
            raise ValueError("No product ID in response")
            
        print(f"✅ Created outlet product with ID: {created_offer_id}")
        
        # Update product details
        self.shoper_products.update_product(created_offer_id, barcode=new_outlet.barcode)
        self.shoper_products.update_product(created_offer_id, related=new_outlet.related)
        
        # Update URL
        product_url_json = {'pl_PL': {'seo_url': new_outlet.product_url(created_offer_id)}}
        self.shoper_products.update_product(created_offer_id, translations=product_url_json)

        # Update images
        outlet_pictures = new_outlet.set_outlet_pictures(created_offer_id)
        for picture in outlet_pictures:
            self.shoper_pictures.update_product_image(created_offer_id, picture)

        # Update stock image
        created_product = self.shoper_products.get_a_product_by_code(created_offer_id)
        if created_product and 'main_image' in created_product:
            stock_gfx = created_product['main_image']['gfx_id']
            self.shoper_products.update_product(created_offer_id, stock={'gfx_id': stock_gfx})
