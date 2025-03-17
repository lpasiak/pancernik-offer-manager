import pandas as pd


class EasyStorageData:

    def __init__(self, file_path):
        self.file_path = file_path
        try:
            self.data = pd.read_excel(file_path)
            print("Easystorage Data downloaded.")
        except Exception as e:
            raise Exception(f"Failed to read Excel file: {str(e)}")
    
    @property
    def outlet_products(self):
        try:
            outlet_filter = (self.data['Strefa'] == 'KMP-OUTLET') & (self.data['Magazyn'] == 'MAG')
            filtered_data = self.data[outlet_filter].copy()  # Create a copy to avoid modifying original
            filtered_data['SKU'] = filtered_data['SKU'].str.upper()
            return filtered_data
        except KeyError as e:
            raise KeyError(f"Required column missing in data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error processing outlet products: {str(e)}")
