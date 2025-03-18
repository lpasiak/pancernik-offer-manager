import config
import pandas as pd

class ShoperCategories:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_categories(self):
        """Get all categories from Shoper and return them as df or None"""
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
                    error_description = response.json()['error_description']
                    print(f'❌ API Error: {error_description}')
                    return {'success': False, 'error': error_description}

                page_data = response.json().get('list', [])

                if not page_data:
                    break
            
                print(f'Page: {page}/{number_of_pages}')
                categories.extend(page_data)
                page += 1
            
            df = pd.DataFrame(categories)
            return df
        
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
    
