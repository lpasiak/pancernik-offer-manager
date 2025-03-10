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

    def get_data(self, sheet_name, include_row_numbers=False):
        """Get data from a Google Sheets worksheet as a pandas DataFrame.
        Args:
            sheet_name (str): Name of the specific sheet.
            include_row_numbers (bool): Whether to include Gsheets row numbers in the DataFrame.
        Returns:
            A pandas DataFrame containing the data from the worksheet or None if an error occurs.
        """
        try:
            self.worksheet = self.sheet.worksheet(sheet_name)
            data = self.worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])  # First row as header
            
            # Making sure the necessary data is properly formatted in gsheets
            if df['SKU']:
                df['SKU'] = df['SKU'].str.upper()
            if df['Uszkodzenie']:
                df['Uszkodzenie'] = df['Uszkodzenie'].str.upper()

            if include_row_numbers:
                df.insert(0, 'Row Number', range(2, len(df) + 2)) # GSheets rows start at 2

            print('Downloaded all the data from Google Sheets.')
            print("-----------------------------------")
            return df
        
        except Exception as e:
            print(f"Error getting data from Google Sheets: {e}")
            return None