import gspread
import pandas as pd
from pathlib import Path
import config

class GSheetsClient:

    def __init__(self, credentials, sheet_id, sheet_name):
        """
        Initialize the GSheetsClient with credentials and sheet ID.
        Args:
            credentials (str): Path to the service account JSON credentials file.
            sheet_id (str): Name of the environment variable storing the sheet ID.
            sheet_name (str): Name of the specific sheet.
        """

        self.credentials_path = credentials
        self.sheet_id = sheet_id
        self.gc = None
        self.sheet = None
        self.sheet_name = sheet_name

        # We will save downloaded data in Excel in 'sheets' directory.
        # It needs to be created if it doesn't exist in our local files.
        self.sheets_dir = Path('sheets')
        self.sheets_dir.mkdir(exist_ok=True)


    def connect(self):
        """Authenticate with Google Sheets."""

        self.gc = gspread.service_account(filename=self.credentials_path)
        self.sheet = self.gc.open_by_key(self.sheet_id)

        print(f"Google Authentication {config.SHEET} | {self.sheet_name} successful.")