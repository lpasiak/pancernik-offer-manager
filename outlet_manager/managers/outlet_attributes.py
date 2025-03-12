from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.attributes import ShoperAttributes
from connections.shoper.categories import ShoperCategories
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config

class OutletAttributeManager:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.shoper_attributes = None
        self.shoper_categories = None
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
            self.shoper_attributes = ShoperAttributes(self.shoper_client)
            self.shoper_categories = ShoperCategories(self.shoper_client)
            
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

    def update_attribute_groups(self):
        """Select all categories and append """
        
        # Get all necessary products
        df_all_products = self.gsheets_worksheets.get_data(sheet_name='Outlety', include_row_numbers=True)
        mask = (
            (df_all_products['ID Shoper'].notna() & df_all_products['ID Shoper'].ne('')) &
            (df_all_products['ID Kategorii'].notna() & df_all_products['ID Kategorii'].ne(''))
        )
        df_all_products = df_all_products[mask]

        # Get unique category list
        category_ids_to_append = df_all_products['ID Kategorii'].astype(int).unique().tolist()

        # Attribute group to append categories to
        attribute_group_to_append = config.OUTLET_MAIN_PRODUCT_ATTRIBUTE_IDS[config.SITE]['group']

        # Get attribute group all categories
        attribute_group_categories = self.shoper_attributes.get_attribute_group_by_id(attribute_group_to_append)['categories']

        # Merge current and new categories
        categories_to_import = sorted(list(set(attribute_group_categories + category_ids_to_append)))

        # Update attribute group categories
        response = self.shoper_attributes.update_attribute_group_categories(attribute_group_to_append, categories_to_import)

        if response:
            print(f'✅ Attribute group {attribute_group_to_append} updated with {len(categories_to_import)} categories')
        else:
            print(f'❌ Attribute group {attribute_group_to_append} update failed')


