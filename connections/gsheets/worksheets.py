from ..gsheets_connect import GSheetsClient
import pandas as pd
import config

class GsheetsWorksheets:

    def __init__(self, client=GSheetsClient):
        """Initialize a Shoper Client"""
        self.client = client

    def get_data(self, sheet_name, include_row_numbers=False):
        """Get data from a Google Sheets worksheet as a pandas DataFrame.
        Args:
            sheet_name (str): Name of the specific sheet.
            include_row_numbers (bool): Whether to include Gsheets row numbers in the DataFrame.
        Returns:
            A pandas DataFrame containing the data from the worksheet or None if an error occurs.
        """
        try:
            self.client.worksheet = self.client.sheet.worksheet(sheet_name)
            data = self.client.worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])  # First row as header
            
            # Making sure the necessary data is properly formatted in gsheets
            if 'SKU' in df.columns:
                df['SKU'] = df['SKU'].str.upper()
                mask = (df['SKU'].notna() & df['SKU'].ne(''))
                df = df[mask]


            if include_row_numbers:
                df.insert(0, 'Row Number', range(2, len(df) + 2)) # GSheets rows start at 2

            df.to_excel(config.SHEETS_DIR / f'gsheets_{sheet_name.lower()}.xlsx', index=False)
            print('Downloaded all the data from Google Sheets.')
            return df
        
        except Exception as e:
            print(f"Error getting data from Google Sheets: {e}")
            return None