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

TODAY = datetime.today().strftime('%d-%m-%Y')

# Load environment variables from .env file
load_dotenv(ENV_FILE)

# Shoper SITE - can be either TEST (development) or MAIN (deployment)
SITE = 'MAIN'
SHOPER_SITE_URL = os.getenv(f'SHOPER_SITE_URL_{SITE}')
SHOPER_LOGIN = os.getenv(f'SHOPER_LOGIN_{SITE}')
SHOPER_PASSWORD = os.getenv(f'SHOPER_PASSWORD_{SITE}')

# Shoper SITE LIMIT for API requests (50 is max)
SHOPER_LIMIT = 50

# PROMOTION MANAGER Google Sheets
PROMO_SHEET_ID = os.getenv('PROMO_SHEET_ID')
PROMO_SHEET_EXPORT_NAME = 'Eksport'
PROMO_SHEET_IMPORT_NAME_PERCENT = 'Do importu procenty'
PROMO_SHEET_IMPORT_NAME = 'Do importu stałe'

# OUTLET MANAGER Google Sheets
OUTLET_SHEET_ID = os.getenv('OUTLET_SHEET_ID')
OUTLET_SHEET_NAME = 'Outlety'
OUTLET_SHEET_LACKING_PRODUCTS_NAME = 'Brak produktów'
OUTLET_SHEET_ARCHIVED_NAME = 'Archiwum'

OUTLET_VALID_DAMAGE_TYPES = ['USZ', 'ZAR', 'OBA']
OUTLET_DISCOUNT_PERCENTAGE = 0.8

OUTLET_ATTRIBUTE_IDS = {
    'MAIN': {'id': '1402', 'group': '577'},
    'TEST': {'id': '29', 'group': '9'}
}

# CLEANUP MANAGER Google Sheets
CLEANUP_SHEET_ID = os.getenv('CLEANUP_SHEET_ID')
CLEANUP_SHEET_DIMENSIONS_NAME = 'Wymiary'
CLEANUP_SHEET_DIMENSIONS_IGNORE_NAME = 'Bez wymiarów'
