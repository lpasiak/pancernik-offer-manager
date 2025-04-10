from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.pictures import ShoperPictures
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
from connections.easystorage_connect import EasyStorageClient
from connections.easystorage.products import EasyStorageProducts
import config


class CleanupManager:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.shoper_pictures = None
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
        
    # def create_a_bundle(self, bundle_id):
    #     product = self.shoper_products.get_product_by_code(bundle_id)

    #     product['code'] = 'TestowyProduktZestawBizon'
    #     product['stock']['code'] = 'TestowyProduktZestawBizon'
    #     product['translations']['pl_PL']['name'] = 'Testowy zestaw Bizon'
    #     product['translations']['pl_PL']['seo_url'] = 'testowy-zestaw-bizon'
        
    #     self.shoper_products.create_product(product)