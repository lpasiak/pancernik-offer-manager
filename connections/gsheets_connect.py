import gspread
import pandas as pd
from pathlib import Path
import config

class GSheetsClient:

    def __init__(self, credentials, sheet_id):
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

    def connect(self):
        """Authenticate with Google Sheets."""

        self.gc = gspread.service_account(filename=self.credentials_path)
        self.sheet = self.gc.open_by_key(self.sheet_id)

        print(f"Google Authentication successful.")
