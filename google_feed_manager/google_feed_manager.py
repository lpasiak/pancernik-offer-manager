
from connections import ShoperAPIClient, GSheetsClient, SubiektClient
from connections.subiekt import SubiektProducts
from connections.shoper.products import ShoperProducts
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd
import json
import re
from tqdm import tqdm


class GoogleCostOfGoodsSold:
    def __init__(self):
        self.shoper_client = None
        self.gsheets_client = None
        self.subiekt_client = None
        self.shoper_products = None
        self.gsheets_worksheets = None
        
        self.subiekt_pancernik_2025 = None
        
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

            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                config.PRICES_SHEET_FOR_COGS_ID
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)

            self.subiekt_client = SubiektClient()
            self.subiekt_client.connect()
            self.subiekt_products = SubiektProducts(self.subiekt_client)

            self.subiekt_pancernik_2025 = pd.DataFrame(self.subiekt_products.get_products(self.subiekt_client.database_2025))
            return True
            
        except Exception as e:
            print(f"❌ Error initializing connections: {e}")
            return False
        
    def _convert_json_to_df(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    # If data is a dictionary, convert its values to a list
                    data = list(data.values())
                elif not isinstance(data, list):
                    # If data is neither dict nor list, wrap it in a list
                    data = [data]
                return pd.DataFrame(data)
        except Exception as e:
            print(f'❌ Error in _convert_json_to_df: {e}')

    def get_all_products_from_shoper_export(self):
        product_df = self._convert_json_to_df(config.SHEETS_DIR / 'api-exports' / 'shoper-beautiful-products.json')

        product_mask = (
            (~product_df['code'].str.contains('szablon', case=False, na=False)) &
            (~product_df['code'].str.contains('out', case=False, na=False)) &
            (product_df['cogs'] == '')
        )

        product_df['code'] = product_df['code'].astype(str)
        product_df = product_df[product_mask]

        return product_df

    def import_bizon_prices_to_shoper(self, product_df):

        try:
            price_df = self.gsheets_worksheets.get_data('Bizon')

            product_df = product_df[product_df['producer'] == 'Bizon']

            price_mask = (
                (price_df['EAN'].notna()) &
                (price_df['EAN'] != '') &
                (price_df['EAN'] != 0) &
                (price_df['EAN'] != '0') &
                (price_df['EAN'] != '#N/A')
            )
            price_df = price_df[price_mask]
            price_df['EAN'] = price_df['EAN'].astype(str)
            
            bizon_product_df = pd.merge(
                product_df,
                price_df,
                left_on='code',
                right_on='EAN',
                how='left'
            )

            bizon_product_df['COGS'] = bizon_product_df['Koszt produkcji netto'].astype(str).str.replace(',', '.') + ' PLN'
            bizon_product_df = bizon_product_df[['product_id', 'COGS', 'Koszt produkcji netto']]

            for _, row in tqdm(bizon_product_df.iterrows(), total=len(bizon_product_df), desc="Updating Bizon products", unit=" product"):
                self.shoper_products.update_product_by_code(row['product_id'], 
                                                            attributes={config.COST_OF_GOODS_SOLD['id']: row['COGS']},
                                                            stock={'price_buying': row['Koszt produkcji netto']})
        except Exception as e:
            print(f'❌ Failed to upload Bizon COGS: {e}')
            
    def import_bewood_dropshipping_prices_to_shoper(self, product_df):

        try:
            price_df = self.gsheets_worksheets.get_data('Bewood', include_row_numbers=False)

            product_mask = (
                (product_df['producer'] == 'Bewood') &
                (product_df['gauge'].str.contains('Wydłużony czas realizacji')) &
                (product_df['series'] != '')
            )

            product_df = product_df[product_mask]

            bewood_product_df = pd.merge(
                        product_df,
                        price_df,
                        left_on='series',
                        right_on='Seria',
                        how='left'
            )

            bewood_product_df['COGS'] = bewood_product_df['Cena zakupu netto'].astype(str).str.replace(',', '.') + ' PLN'
            bewood_product_df = bewood_product_df[['product_id', 'COGS', 'Cena zakupu netto']]

            for _, row in tqdm(bewood_product_df.iterrows(), total=len(bewood_product_df), desc="Updating Bewood drop products", unit=" product"):
                self.shoper_products.update_product_by_code(row['product_id'], 
                                                            attributes={config.COST_OF_GOODS_SOLD['id']: row['COGS']},
                                                            stock={'price_buying': row['Cena zakupu netto']})
        except Exception as e:
            print(f'❌ Failed to upload Bewood Drop COGS: {e}')

    def import_grizz_dropshipping_prices_to_shoper(self, product_df):

        try:
            product_mask = (
                (product_df['producer'] == 'GrizzProtector') &
                (product_df['gauge'].str.contains('Wydłużony czas realizacji'))
            )

            product_df = product_df[product_mask].copy()

            product_df['price'] = product_df['price'].astype(float)
            product_df['bought_net_price'] = product_df['price'].map(lambda price: round((price * 0.68) / 1.23, 2))
            product_df['COGS'] = product_df['bought_net_price'].astype(str).str.replace(',', '.') + ' PLN'

            product_df = product_df[['product_id', 'COGS', 'bought_net_price']]

            for _, row in tqdm(product_df.iterrows(), total=len(product_df), desc="Updating Grizz drop products", unit=" product"):
                self.shoper_products.update_product_by_code(row['product_id'], 
                                                            attributes={config.COST_OF_GOODS_SOLD['id']: row['COGS']},
                                                            stock={'price_buying': row['bought_net_price']})

        except Exception as e:
            print(f'❌ Failed to upload Grizz Drop COGS: {e}')
