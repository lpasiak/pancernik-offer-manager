import os
from pathlib import Path

# Shoper SITE - can be either TEST (development) or MAIN (deployment)
SITE = 'MAIN'

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

# CLEANUP MANAGER Google Sheets
CLEANUP_SHEET_ID = os.getenv('CLEANUP_SHEET_ID')
CLEANUP_SHEET_DIMENSIONS_NAME = 'Wymiary'
CLEANUP_SHEET_DIMENSIONS_IGNORE_NAME = 'Bez wymiarów'

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# GSheets credentials file
CREDENTIALS_FILE = ROOT_DIR / 'credentials' / 'gsheets_credentials.json'

# Directory for .xlsx, .csv, .json files
SHEETS_DIR = ROOT_DIR / 'sheets'
