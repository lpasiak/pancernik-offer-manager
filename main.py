from connections.gsheets_connect import GSheetsClient
from outlet_manager import outlet_manager
import config

gsheets_client = GSheetsClient(
    credentials=config.GOOGLE_CREDENTIALS_FILE,
    sheet_id=config.OUTLET_SHEET_ID
)

gsheets_client.connect()

outlet_manager.create_outlet_offers()