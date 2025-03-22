import gspread
import pandas as pd
from pathlib import Path
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
        max_retries = 20
        retry_count = 0
        base_delay = 20  # Start with 20 seconds delay

        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except gspread.exceptions.APIError as e:
                retry_count += 1
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    delay = base_delay * (2 ** (retry_count - 1))  # Exponential backoff
                    print(f"API quota exceeded. Waiting {delay} seconds before retry {retry_count}/{max_retries}...")
                    time.sleep(delay)
                else:
                    raise  # Re-raise if it's a different API error
            except Exception as e:
                raise  # Re-raise any other exceptions

        raise Exception(f"Failed after {max_retries} retries")

    def connect(self):
        """Authenticate with Google Sheets."""

        self.gc = gspread.service_account(filename=self.credentials_path)
        self.sheet = self.gc.open_by_key(self.sheet_id)

        print(f"Google Authentication successful.")
