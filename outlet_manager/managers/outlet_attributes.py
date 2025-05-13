from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.attributes import ShoperAttributes
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd
from utils.logger import get_outlet_logger


class OutletAttributeManager:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.shoper_attributes = None
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
            self.shoper_attributes = ShoperAttributes(self.shoper_client)
            
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
            self.outlet_logger.warning(f'❌ Error initializing connections: {e}')
            return False

    def select_products_with_ids(self):
        """Get all products with ID and category
        Returns:
            pd.DataFrame: DataFrame with products that have ID and category
            """
        df_all_products = self.gsheets_worksheets.get_data(sheet_name=config.OUTLET_SHEET_NAME, include_row_numbers=True)
        mask = (
            (df_all_products['ID Shoper'].notna() & df_all_products['ID Shoper'].ne('')) &
            (df_all_products['ID Kategorii'].notna() & df_all_products['ID Kategorii'].ne(''))
        )

        return df_all_products[mask]

    def update_attribute_groups(self):
        """Select all categories from the gsheets and append them to the attribute group"""
        
        # Get all necessary products
        df_all_products = self.select_products_with_ids()

        # Get unique category list
        category_ids_to_append = df_all_products['ID Kategorii'].astype(int).unique().tolist()
        category_ids_to_append = [int(i) for i in category_ids_to_append]
        
        # Attribute group to append categories to
        attribute_group_to_append = config.OUTLET_MAIN_PRODUCT_ATTRIBUTE_IDS[config.SITE]['group']

        # Get attribute group all categories
        attribute_group_categories = self.shoper_attributes.get_attribute_group_by_id(attribute_group_to_append)['categories']
        attribute_group_categories = [int(i) for i in attribute_group_categories]

        # Merge current and new categories
        categories_to_import = sorted(list(set(attribute_group_categories + category_ids_to_append)))

        # Update attribute group categories
        response = self.shoper_attributes.update_attribute_group_categories(attribute_group_to_append, categories_to_import)

        if response:
            print(f'✅ Attribute group {attribute_group_to_append} updated with {len(categories_to_import)} categories\n')
            self.outlet_logger.info(f'✅ Attribute group {attribute_group_to_append} updated with {len(categories_to_import)} categories')
        else:
            print(f'❌ Attribute group {attribute_group_to_append} update failed')
            self.outlet_logger.warning(f'❌ Attribute group {attribute_group_to_append} update failed')

    def update_main_products_attributes(self):
        """Update the attribute of a product"""

        # Get all necessary products
        df_all_products = self.select_products_with_ids()

        # Remove duplicated EANs
        single_ean_products = df_all_products.drop_duplicates(subset=['EAN'], keep='first').copy()

        # Get the attribute ID
        attribute_id = config.OUTLET_MAIN_PRODUCT_ATTRIBUTE_IDS[config.SITE]['id']

        # Create a dictionary of products with EAN as key and list of IDs as value
        products = {}
        product_counter = 0

        # Create a dictionary of products with EAN as key and list of IDs as value
        for _, row_single in single_ean_products.iterrows():
            product_ean = row_single['EAN']
            product_ids_list = df_all_products[df_all_products['EAN'] == product_ean]['ID Shoper'].tolist()
            if product_ids_list:
                products[product_ean] = ', '.join(map(str, product_ids_list))
        
        print(f'Updating {len(products)} main products attributes:\n')

        # Update the attribute of the product
        for product_ean, product_ids in products.items():
            params = {attribute_id: product_ids}
            self.shoper_products.update_product_by_code(product_ean, use_code=True, attributes=params)
            product_counter += 1
            print(f'✅ Products updated: {product_counter}/{len(products)}')
        
        self.outlet_logger.info(f'✅ Product attributes updated: {product_counter}/{len(products)}')

