from ..shoper_connect import ShoperAPIClient
import config, os
import pandas as pd

class ShoperCategories:

    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_categories(self):
        """Get all categories from Shoper and return them as df or None and save to Excel."""
        try:
            print("Downloading all categories.")

            categories = []
            page = 1

            while True:
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/categories', params=params)
                data = response.json()
                number_of_pages = data['pages']

                if response.status_code != 200:
                    print(f'❌ API Error: {response.status_code}, {response.text}')
                    return None

                page_data = response.json().get('list', [])

                if not page_data:
                    break
            
                print(f'Page: {page}/{number_of_pages}')
                categories.extend(page_data)
                page += 1
            
            df = pd.DataFrame(categories)
            df.to_excel(config.SHEETS_DIR / 'shoper_all_categories.xlsx', index=False)
            return df
        
        except Exception as e:
            print(f'❌ Error fetching all categories: {str(e)}')
            return None
    
