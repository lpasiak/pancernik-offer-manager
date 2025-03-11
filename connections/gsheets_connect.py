import gspread
import pandas as pd
from pathlib import Path
import config
import time

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

    def _handle_request(self, func, *args, **kwargs):
        """
        Handle Google Sheets API requests with automatic retry on quota exceeded errors.
        Args:
            func: The gspread function to execute
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
        Returns:
            The result of the API call
        """
        while True:
            try:
                return func(*args, **kwargs)
            except gspread.exceptions.APIError as e:
                if "RESOURCE_EXHAUSTED" in str(e):
                    print("API quota exceeded. Waiting 1 second before retry...")
                    time.sleep(1)  # Wait 100 seconds before retrying
                else:
                    raise  # Re-raise if it's a different API error


    def connect(self):
        """Authenticate with Google Sheets."""

        self.gc = gspread.service_account(filename=self.credentials_path)
        self.sheet = self.gc.open_by_key(self.sheet_id)

        print(f"Google Authentication successful.")
