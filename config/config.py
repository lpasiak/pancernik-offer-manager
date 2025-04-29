from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import os

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# Credentials files
GOOGLE_CREDENTIALS_FILE = ROOT_DIR / 'credentials' / 'gsheets_credentials.json'
ENV_FILE = ROOT_DIR / 'credentials' / 'env'

# Directory for .xlsx, .csv, .json files
SHEETS_DIR = ROOT_DIR / 'sheets'
DRIVE_EXPORT_DIR = r'H:\Pansernik\Eksporty'

TODAY = datetime.today().strftime('%d-%m-%Y')

REDIRECT_TARGET_OUTLET_URL = '/outlet'

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Shoper SITE - can be either TEST (development) or MAIN (deployment)
SITE = 'MAIN'
SHOPER_SITE_URL = os.getenv(f'SHOPER_SITE_URL_{SITE}')
SHOPER_LOGIN = os.getenv(f'SHOPER_LOGIN_{SITE}')
SHOPER_PASSWORD = os.getenv(f'SHOPER_PASSWORD_{SITE}')

# Shoper SITE LIMIT for API requests (50 is max)
SHOPER_LIMIT = 50

# Shopify SITE
SHOPIFY_CREDENTIALS = {
    'api_key': os.getenv('SHOPIFY_API_KEY'),
    'api_secret': os.getenv('SHOPIFY_API_SECRET'),
    'api_token': os.getenv('SHOPIFY_API_TOKEN'),
    'shop_url': os.getenv('SHOPIFY_URL')
}
SHOPIFY_API_VERSION = '2025-04'

# IDOSELL SITE
IDOSELL_SANDBOX_SITE = os.getenv('IDOSELL_SANDBOX_SITE')
IDOSELL_SANDBOX_API_KEY = os.getenv('IDOSELL_SANDBOX_API_KEY')

IDOSELL_BIZON_RETAIL_SITE = os.getenv('IDOSELL_RETAIL_SITE')
IDOSELL_BIZON_B2B_SITE = os.getenv('IDOSELL_B2B_SITE')
IDOSELL_API_KEY = os.getenv('IDOSELL_API_KEY')
IDOSELL_API_VERSION = 'v5'

# Allegro SITE
ALLEGRO_API_SECRET_SANDBOX = os.getenv('ALLEGRO_API_SECRET_SANDBOX')

# Easystorage API
EASYSTORAGE_CREDENTIALS = {
    'username': os.getenv('EASYSTORAGE_LOGIN'),
    'password': os.getenv('EASYSTORAGE_PASSWORD')
}

# PROMOTION MANAGER Google Sheets
PROMO_SHEET_ID = os.getenv('PROMO_SHEET_ID')
PROMO_SHEET_EXPORT_NAME = 'Eksport'
PROMO_SHEET_IMPORT_NAME_PERCENT = 'Do importu procenty'
PROMO_SHEET_KUBA = 'KubaBuba'
PROMO_SHEET_TO_REMOVE = 'Do usunięcia'
PROMO_TIME_END = '2031-12-31'

# OUTLET MANAGER Google Sheets
OUTLET_SHEET_ID = os.getenv('OUTLET_SHEET_ID')
OUTLET_SHEET_NAME = 'Outlety'
OUTLET_SHEET_LACKING_PRODUCTS_NAME = 'Brak produktów'
OUTLET_SHEET_ARCHIVED_NAME = 'Archiwum'

OUTLET_VALID_DAMAGE_TYPES = ['USZ', 'ZAR', 'OBA']
OUTLET_DISCOUNT_PERCENTAGE = 20
OUTLET_DAYS_TO_DISCOUNT = 14
OUTLET_DAYS_TO_BE_REMOVED = 60

OUTLET_MAIN_PRODUCT_ATTRIBUTE_IDS = {
    'MAIN': {'id': '1402', 'group': '577'},
    'TEST': {'id': '29', 'group': '9'}
}

PRODUCT_TYPE = {
    'MAIN': {'id': '1370', 'group': '550'},
    'TEST': {'id': '28', 'group': '8'}
}

# CLEANUP MANAGER Google Sheets
CLEANUP_SHEET_ID = os.getenv('CLEANUP_SHEET_ID')
CLEANUP_SHEET_DIMENSIONS_NAME = 'Wymiary'
CLEANUP_SHEET_DIMENSIONS_IGNORE_NAME = 'Bez wymiarów'
CLEANUP_ALLEGRO_TITLES_NAME = 'Nazwy Allegro'
MISSING_ALLEGRO_OFFERS_NAME = 'Uzupełnianie Allegro | sklep-pancernik'
MISSING_SHOPIFY_OFFERS_NAME = 'Uzupełnianie Shopify'
MISSING_ATTRIBUTES_NAME = 'Uzupełnianie Atrybuty'
CLEANUP_ARCHIVED_NAME = 'Archiwum'