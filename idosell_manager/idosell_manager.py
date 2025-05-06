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
            # Initialize Shoper connections
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
            print(f"Error initializing connections: {e}")
            return False
        
    def get_sheets_data(self):
        """Download Product Info from Google Sheets as a DataFrame"""
        selected_data = self.gsheets_worksheets.get_data(sheet_name=config.BIZON_PRODUCT_INFO)
        return selected_data

    def get_idosell_product_codes(self):
        """Export all the products and its identifiers: id, product_code, external_code"""
        selected_data = self.idosell_products.get_all_product_codes()
        return selected_data

    def select_products_to_update(self):
        """Creates a DataFrame of all the products exported from IdoSell and Gsheets
            - product_codes
            - dimensions
            - last delivery price
            - weight
        """
        gsheets_data = self.get_sheets_data()
        idosell_data = pd.DataFrame(self.get_idosell_product_codes())

        merged_df = pd.merge(
            idosell_data,
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

        merged_df.to_excel('test.xlsx', index=False)
        return merged_df


    def upload_product_information(self):
        """Update products with their Purchase Price, Weight and Dimensions"""
        products_to_update = self.select_products_to_update()
        products_length = len(products_to_update)

        for index, row in products_to_update.iterrows():

            product_price = float(row['Koszt produkcji brutto'].replace(',', '.'))

            try:
                response = self.idosell_products.update_product_logistic_info(
                    product_id=int(row['product_id']),
                    product_external_code=str(row['product_external_code']),
                    purchase_price_gross=product_price,
                    weight=int(row['Waga brutto']),
                    width=float(row['Szerokość']),
                    height=float(row['Wysokość']),
                    length=float(row['Długość'])
                )

                print(f'Updated product {row['product_id']} with:\t\t|{index+1}/{products_length}')
                print(f'Price: {product_price} | Weight: {row['Waga brutto']} | Dimensions: {row['Długość']}x{row["Szerokość"]}x{row["Szerokość"]}')

            except Exception as e:
                print(print(f'❌ Request failed: {str(e)}'))
