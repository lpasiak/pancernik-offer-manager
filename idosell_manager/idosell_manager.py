from connections.idosell_connect import IdoSellAPIClient
from connections.idosell.products import IdoSellProducts
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd


class IdoSellManager:
    def __init__(self):
        self.idosell_client = None
        self.gsheets_client = None
        self.idosell_products = None
        self.gsheets_worksheets = None
        
    def connect(self):
        """Initialize all necessary connections"""
        try:
            # Initialize IdoSell connections
            self.idosell_client = IdoSellAPIClient(
                api_key=config.IDOSELL_API_KEY,
                site=config.IDOSELL_BIZON_B2B_SITE
            )
            self.idosell_client.connect()
            self.idosell_products = IdoSellProducts(self.idosell_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.BIZON_SHEET_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            return False

    def select_products_to_update(self):
        """Creates a DataFrame of all the products exported from IdoSell and Gsheets
            - product_codes
            - dimensions
            - last delivery price
            - weight
        """
        gsheets_data = self.gsheets_worksheets.get_data(sheet_name=config.BIZON_PRODUCT_INFO)
        idosell_json = self.idosell_products.get_all_products_logistic_info()
        idosell_data = pd.DataFrame(idosell_json)

        # Select products to update
        columns_to_check = ['purchase_price_gross_last', 'weight', 'length', 'width', 'height']
        filtered_idosell_data = idosell_data[(idosell_data[columns_to_check] == 0).any(axis=1)]

        merged_df = pd.merge(
            filtered_idosell_data,
            gsheets_data,
            left_on='product_code',
            right_on='EAN',
            how='inner'
        )

        columns_to_keep = ['product_id',
                           'product_code',
                           'product_external_code',
                           'Waga brutto',
                           'Długość',
                           'Wysokość',
                           'Szerokość',
                           'Koszt produkcji brutto']
        
        merged_df = merged_df[columns_to_keep]

        merged_df = merged_df.apply(
            lambda col: col.map(
                lambda x: 0 if pd.isna(x) or str(x).strip().lower() in ['', 'nan', 'none', 'null'] else x
            )
        )

        print(f'ℹ️  {len(merged_df)} offers to update.')
        return merged_df

    def upload_product_information(self):
        """Update products with their Purchase Price, Weight and Dimensions"""
        products_to_update = self.select_products_to_update()
        products_length = len(products_to_update)
        products_updated = 0

        for index, row in products_to_update.iterrows():

            try:

                product_price = float(row['Koszt produkcji brutto'].replace(',', '.'))
                product_weight = int(round(float(str(row['Waga brutto']).replace(',', '.'))))

                # If product weight is null, let's import 200 gram
                if product_weight == 0:
                    product_weight = 200

                response = self.idosell_products.update_product_logistic_info(
                    product_id=int(row['product_id']),
                    product_external_code=str(row['product_external_code']),
                    purchase_price_gross=product_price,
                    weight = product_weight,
                    width=float(row['Szerokość']),
                    height=float(row['Wysokość']),
                    length=float(row['Długość'])
                )

                if response.status_code == 200 or response.status_code == 207:
                    print(f'✅ Updated product {row['product_id']} with:\t\t|{index+1}/{products_length}')
                    print(f'Price: {product_price}')
                    print(f'Weight: {product_weight}')
                    print(f'Dimensions: {row['Długość']}x{row["Szerokość"]}x{row["Szerokość"]}')
                    products_updated = products_updated + 1
                    
                else:
                    print(f'Failed to update product {row['product_id']}')

            except Exception as e:
                print(f'❌ Failed to update product {row['product_id']}')
                print(f'❌ Request failed: {str(e)}')

        print(f'Summary: Updated {products_updated}/{products_length} products.')
