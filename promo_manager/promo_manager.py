from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.specialoffers import ShoperSpecialOffers
from connections.gsheets_connect import GSheetsClient
from connections.gsheets.worksheets import GsheetsWorksheets
import config
import pandas as pd
from tqdm import tqdm
from utils.logger import get_promo_logger


class PromoManager:
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.shoper_client = None
        self.gsheets_client = None
        self.shoper_products = None
        self.gsheets_worksheets = None
        self.promo_logger = get_promo_logger().get_logger()
        
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
            self.shoper_special_offers = ShoperSpecialOffers(self.shoper_client)
            
            # Initialize Google Sheets connections
            self.gsheets_client = GSheetsClient(
                config.GOOGLE_CREDENTIALS_FILE,
                '1Tn0pmuHs9yXQvIZxwxp8VOK6v4CGNMWx5ixeTHQ6vZc'
                # self.sheet_id
            )
            self.gsheets_client.connect()
            self.gsheets_worksheets = GsheetsWorksheets(self.gsheets_client)
            
            return True
            
        except Exception as e:
            print(f'❌ Error initializing connections: {e}')
            return False
        
    def export_all_promo_products(self):
        """Get all products from shoper and save them to Excel and promo gsheet"""
        df = self.shoper_products.get_all_products()

        # Get only products with promo price
        df = df[df['promo_price'].notna()]

        # Get necessary columns
        df['product_name'] = df['translations'].apply(lambda x: x['pl_PL']['name'])
        df['price'] = df['stock'].apply(lambda x: x['price'])
        df['promo_price'] = df['promo_price']
        df['date_from'] = df['special_offer'].apply(lambda x: x['date_from'])
        df['date_to'] = df['special_offer'].apply(lambda x: pd.to_datetime(x['date_to']).strftime('%Y-%m-%d'))
        df['discount_type'] = df['special_offer'].apply(lambda x: x['discount_type'])
        df['discount_type'] = df['discount_type'].apply(lambda x: 'stały' if x == '2' else 'procentowy' if x == '3' else 'stały' if x == '1' else x)
        df['discount_amount'] = df['special_offer'].apply(lambda x: x['discount'])
        
        # Filter out products that contain 'OUT' in code
        df = df[~df['code'].str.contains('OUT', case=False, na=False)]

        new_df = pd.DataFrame({
            'SKU': df['code'].astype('object'),
            'Nazwa': df['product_name'].astype('object'), 
            'Cena': df['price'].astype('object'),
            'Cena promo': df['promo_price'].astype('object'),
            'Kwota promocji': df['discount_amount'].astype('object'),
            'Typ promocji': df['discount_type'].astype('object'),
            'Data początku': df['date_from'].astype('object'),
            'Data końca': df['date_to'].astype('object'),
            'ID produktu': df['product_id'].astype('object')
        })

        # Save to promo sheets
        self.gsheets_worksheets.save_data(config.PROMO_SHEET_EXPORT_NAME, new_df)

    def import_promo_percent_from_gsheet(self):
        """Create special offers and remove current ones if they exist, get data from google sheet"""

        # Select data to import
        df = self.gsheets_worksheets.get_data(config.PROMO_SHEET_IMPORT_NAME_PERCENT, include_row_numbers=True)
        mask = (
            (~df['Komunikat promocji'].str.contains('Promocja dodana', na=False)) &
            (df['Kwota promocji (%)'].notna())
        )
        df = df[mask]

        result_df = df.copy()
        result_df['Komunikat promocji'] = ''

        counter_products = len(result_df)
        counter = 0
        # Import special offers
        for id, row in tqdm(result_df.iterrows(), total=counter_products, desc='🔁 Creating promotions', unit=' product'):
            try:
                product = self.shoper_products.get_product_by_code(row['SKU'], use_code=True)
                product_id = product['product_id']

                discount_data = {
                    'product_id': product_id,
                    'discount': row['Kwota promocji (%)'],
                    'discount_type': 3,
                    'date_to': config.PROMO_TIME_END
                }

                if product.get('special_offer') is not None:
                    self.shoper_special_offers.remove_special_offer_from_product(product_id)

                try:
                    response = self.shoper_special_offers.create_special_offer(discount_data)

                    if isinstance(response, int):
                        result_df.at[id, 'Komunikat promocji'] = f'Promocja dodana dla {row['SKU']}. Nr promocji: {response}'
                        counter += 1

                except Exception as e:
                    self.promo_logger.warning(f'❌ Error (create offer): {e}')
                    result_df.at[id, 'Komunikat promocji'] = f'Błąd przy tworzeniu promocji: {str(e)}'

            except Exception as e:
                self.promo_logger.warning(f'❌ Error (get product): {e}')
                result_df.at[id, 'Komunikat promocji'] = f'Błąd przy pobieraniu produktu: {str(e)}'

        # Prepare updates in correct format
        updates = []
        for _, row in result_df.iterrows():
            updates.append([
                int(row['Row Number']),
                row['Komunikat promocji']
            ])

        # Update the worksheet
        self.gsheets_worksheets.batch_update_from_a_list(
            worksheet_name = config.PROMO_SHEET_IMPORT_NAME_PERCENT,
            updates = updates,
            start_column = 'E',
        )

    def update_product_stock_from_gsheet(self):
        """Update product stock, get data from google sheet"""

        # Select data to import
        df = self.gsheets_worksheets.get_data(config.PROMO_SHEET_IMPORT_NAME_PERCENT, include_row_numbers=True)
        mask = (
            (~df['Komunikat Stan'].str.contains('Stan zaktualizowany', na=False)) &
            (df['Stan'].notna())
        )
        df = df[mask]

        result_df = df.copy()
        result_df['Komunikat Stan'] = ''

        counter_products = len(result_df)
        counter = 0
        # Import special offers
        for id, row in tqdm(result_df.iterrows(), total=counter_products, desc='📦 Updating stock', unit=' product'):
            try:
                # Update product stock by code
                response = self.shoper_products.update_product_by_code(
                    row['SKU'],
                    use_code=True,
                    stock={'stock': row['Stan']}
                )

                if isinstance(response, int):
                    result_df.at[id, 'Komunikat Stan'] = f'Stan zaktualizowany dla {row['SKU']}. Stan: {row['Stan']}'
                    counter += 1

            except Exception as e:
                self.promo_logger.warning(f'❌ Error: {e}')
                result_df.at[id, 'Komunikat Stan'] = f'Błąd przy aktualizacji stanu: {str(e)}'

        # Prepare updates in correct format
        updates = []
        for _, row in result_df.iterrows():
            updates.append([
                int(row['Row Number']),
                row['Komunikat Stan']
            ])
            
        # Update the worksheet
        self.gsheets_worksheets.batch_update_from_a_list(
            worksheet_name = config.PROMO_SHEET_IMPORT_NAME_PERCENT,
            updates = updates,
            start_column = 'D',
        )

    def remove_promo_offers_from_gsheet(self):
        """Remove promo offers, get data from google sheet"""

        df = self.gsheets_worksheets.get_data(config.PROMO_SHEET_TO_REMOVE, include_row_numbers=True)

        df = df[~df['Komunikat'].str.contains('Oferta usunięta', na=False)]

        result_df = df.copy()
        result_df['Komunikat'] = ''

        counter_products = len(result_df)
        counter = 0

        for id, row in result_df.iterrows():
            try:
                product = self.shoper_products.get_product_by_code(row['SKU'], use_code=True)
                product_id = product['product_id']

                if product.get('special_offer') is not None:
                    # Remove the special offer
                    self.shoper_special_offers.remove_special_offer_from_product(product_id)

                    result_df.at[id, 'Komunikat'] = f'Oferta usunięta - {row['SKU']}'
                    counter += 1
                    print(f'Products: {counter}/{counter_products}')
                else:
                        result_df.at[id, 'Komunikat'] = f'Błąd  {row['SKU']}'
                
            except Exception as e:
                self.promo_logger.warning(f'❌ Error: {e}')
                result_df.at[id, 'Komunikat'] = f'Błąd przy usuwaniu oferty: {str(e)}'

        updates = []
        for _, row in result_df.iterrows():
            updates.append([
                int(row['Row Number']),
                row['Komunikat']
            ])

        self.gsheets_worksheets.batch_update_from_a_list(
            worksheet_name = config.PROMO_SHEET_TO_REMOVE,
            updates = updates,
            start_column = 'B',
        )

    def import_promo_fixed_from_gsheet(self):
        """Create special offers and remove current ones if they exist, get data from google sheet"""

        # Select data to import
        df = self.gsheets_worksheets.get_data(config.PROMO_SHEET_KUBA, include_row_numbers=True)
        mask = (
            (~df['Komunikat'].str.contains('Promocja dodana', na=False)) &
            (df['Cena promocyjna'].notna())
        )
        df = df[mask]

        result_df = df.copy()
        result_df['Komunikat'] = ''
        result_df['Data końca promocji'] = pd.to_datetime(result_df['Data końca promocji'], dayfirst=True).dt.strftime('%Y-%m-%d')
        result_df['Data rozpoczęcia promocji'] = pd.Timestamp.now().strftime('%Y-%m-%d')

        counter_products = len(result_df)
        counter = 0
        # Import special offers
        for id, row in result_df.iterrows():

            try:
                product = self.shoper_products.get_product_by_code(row['SKU'], use_code=True)
                discount_amount = float(row['Cena produktu']) - float(row['Cena promocyjna']) 

                product_id = product['product_id']
                
                discount_data = {
                    'product_id': product_id,
                    'discount': discount_amount,
                    'discount_type': 2,
                    'date_from': row['Data rozpoczęcia promocji'],
                    'date_to': row['Data końca promocji'],
                }

                if product.get('special_offer') is not None:
                    # Remove the special offer
                    self.shoper_special_offers.remove_special_offer_from_product(product_id)

                try:
                    # Create the special offer
                    response = self.shoper_special_offers.create_special_offer(discount_data)
                    
                    if isinstance(response, int):
                        result_df.at[id, 'Komunikat'] = f'Promocja dodana dla {row['SKU']}. Nr promocji: {response}'
                        counter += 1
                        print(f'Products: {counter}/{counter_products}')

                except Exception as e:
                    self.promo_logger.warning(f'❌ Error: {e}')
                    result_df.at[id, 'Komunikat'] = f'Błąd przy tworzeniu promocji: {str(e)}'

            except Exception as e:
                self.promo_logger.warning(f'❌ Error: {e}')
                result_df.at[id, 'Komunikat'] = f'Błąd przy pobieraniu produktu: {str(e)}'

            # Prepare updates in correct format
            updates = []
            for _, row in result_df.iterrows():
                updates.append([
                    int(row['Row Number']),
                    row['Komunikat']
                ])

        # Update the worksheet
        self.gsheets_worksheets.batch_update_from_a_list(
            worksheet_name = config.PROMO_SHEET_KUBA,
            updates = updates,
            start_column = 'E',
        )

    def allegro_discount_offers(self):
        
        today = config.TODAY_PD

        # Get all promotions
        df = self.gsheets_worksheets.get_data(sheet_name=config.ALLEGRO_PROMO_SHEET_NAME, include_row_numbers=True)
        
        df['Data startu'] = pd.to_datetime(
            df['Data rozpoczęcia'], 
            format='%Y-%m-%d',
            errors='coerce')

        df['Data zakończenia'] = pd.to_datetime(
            df['Data zakończenia'], 
            format='%d-%m-%Y',
            errors='coerce')

        df['EAN'] = df['EAN'].str.strip()

        df = df[df['EAN'] != '#N/A']

        df['Cena bazowa'] = df['Cena bazowa'].str.replace('zł', '').str.strip().str.replace(',', '.').astype(float)
        df['Cena promo'] = df['Cena promo'].str.replace('zł', '').str.strip().str.replace(',', '.').astype(float)

        days_difference = (today - df['Data startu']).dt.days
        
        # DEBUG
        df = df.head(5)
        
        offers_too_early_to_discount_mask = (
            (df['Promocja'].str.contains('Utworzona', na=False) == False) &
            (df['Promocja'].str.contains('Pominięta', na=False) == False) &
            (df['Promocja'].str.contains('Error', na=False) == False) &
            (days_difference < 0))
        offers_too_early_to_discount = df[offers_too_early_to_discount_mask]


        for _, row in offers_too_early_to_discount.iterrows():
            self.promo_logger.info(f'ℹ️ {row['EAN']} Offer is too early for a discount.')

        discounts_ommited_too_early = len(offers_too_early_to_discount)

        offers_to_discount_mask = (
            (df['Promocja'].str.contains('Utworzona', na=False) == False) &
            (df['Promocja'].str.contains('Pominięta', na=False) == False) &
            (df['Promocja'].str.contains('Error', na=False) == False) &
            (days_difference >= 0))
        offers_to_discount = df[offers_to_discount_mask]
        
        offers_to_discount_counter = len(offers_to_discount)

        discounts_created = 0
        discounts_ommited = 0
        updates = []

        # DEBUG
        i = 0

        # Processing offers, that have a proper date
        for _, row in tqdm(offers_to_discount.iterrows(), total=offers_to_discount_counter,
                           desc="Processing offers to discount", unit=" product"):
            
            try:
                product = self.shoper_products.get_product_by_code(row['EAN'], use_code=True)

                # Ommit offers that have special offer
                if product.get('special_offer') is not None:
                    self.promo_logger.info(f'⚠️ {row['EAN']} Offer already has a special offer')
                    
                    updates.append([
                        int(row['Row Number']),
                        'Pominięta'
                    ])

                    discounts_ommited = discounts_ommited + 1
                    
                else:
                    # Create offers
                    product_price = float(product['stock']['price'])
                                          
                    if row['Cena promo'] >= product_price and row['Cena bazowa'] >= product_price:
                        self.promo_logger.warning(f'❌ {row['EAN']} Offer has higher price than bazowa and promo.')
                    
                        updates.append([
                            int(row['Row Number']),
                            f'Error | cena produktu jest niższa'
                        ])
                        continue
                        
                    elif row['Cena promo'] > row['Cena bazowa']:
                        discount_type = 'Bazowa'
                        discount = round(product_price - row['Cena bazowa'], 2)
                    else:
                        discount_type = 'Promo'
                        discount = round(product_price - row['Cena promo'], 2)

                    # special_offer_id = self.shoper_special_offers.create_special_offer(
                    #     product_id=product['product_id'],
                    #     discount=discount,
                    #     discount_type=2,
                    #     date_to=row['Data zakończenia']
                    # )

                    # DEBUG
                    i = i + 1
                    special_offer_id = i
                
                    if isinstance(special_offer_id, int):
                        
                        self.promo_logger.info(f'✅ {row['EAN']} Offer created with a discount {discount} | {discount_type}')
                        discounts_created = discounts_created + 1

                        updates.append([
                            int(row['Row Number']),
                            f'Utworzona | zniżka: {discount}'
                        ])

            except Exception:
                updates.append([
                    int(row['Row Number']),
                    f'Error'
                ])      

        self.gsheets_worksheets.batch_update_from_a_list(
            worksheet_name = config.ALLEGRO_PROMO_SHEET_NAME,
            updates = updates,
            start_column = 'L',
        )

        return discounts_created, discounts_ommited, discounts_ommited_too_early

# Offers already created or ommited
    # Do nothing
# Offers missing, that had "Promocja Utworzona"
    # Remove them