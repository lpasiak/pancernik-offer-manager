import pandas as pd
import config

class GsheetsWorksheets:

    def __init__(self, client):
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
            self.client.worksheet = self.client._handle_request(
                self.client.sheet.worksheet,
                sheet_name
            )
            data = self.client._handle_request(
                self.client.worksheet.get_all_values
            )
            
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

    def batch_update_from_a_list(self, worksheet_name: str, updates: list, start_column: str = 'A', num_columns: int = 5):
        """Batch update multiple rows in a worksheet.
        Args:
            worksheet_name (str): Name of the worksheet to update
            updates (list): List of tuples containing (row_number, value1, value2, ...)
            start_column (str, optional): Starting column letter. Defaults to 'A'.
            num_columns (int, optional): Number of columns to update. Defaults to 5.
        """
        try:
            worksheet = self.client.sheet.worksheet(worksheet_name)
            batch_data = []
            
            # Calculate end column letter
            end_column = chr(ord(start_column.upper()) + num_columns - 1)
            
            for row_data in updates:
                row_number = row_data[0]
                values = row_data[1:]
                
                batch_data.append({
                    'range': f"{start_column}{row_number}:{end_column}{row_number}",
                    'values': [list(values)]
                })

            if batch_data:
                worksheet.batch_update(batch_data)
                print(f"✓ Successfully updated {len(updates)} rows in {worksheet_name}")
            
        except Exception as e:
            print(f"Failed to update worksheet: {str(e)}")
            raise
