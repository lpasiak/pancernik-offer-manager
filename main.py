from connections.shoper_connect import ShoperAPIClient
from connections.shoper.products import ShoperProducts
from connections.shoper.attributes import ShoperAttributes
from connections.shoper.categories import ShoperCategories
from connections.gsheets_connect import GSheetsClient
from outlet_manager import outlet_manager
import config
import pandas as pd

shoper_client = ShoperAPIClient(
    site_url=config.SHOPER_SITE_URL,
    login=config.SHOPER_LOGIN,
    password=config.SHOPER_PASSWORD
)

gsheets_client = GSheetsClient(
    credentials=config.GOOGLE_CREDENTIALS_FILE,
    sheet_id=config.OUTLET_SHEET_ID
)

gsheets_client.connect()
shoper_client.connect()
shoper_products = ShoperProducts(shoper_client)
shoper_attributes = ShoperAttributes(shoper_client)
shoper_categories = ShoperCategories(shoper_client)

# shoper_categories.get_all_categories()

outlet_manager.display_outlets_to_create()