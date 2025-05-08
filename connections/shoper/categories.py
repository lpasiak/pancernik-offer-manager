import config
import pandas as pd
from tqdm import tqdm


class ShoperCategories:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_categories(self):
        """Get all categories from Shoper and return them as df or None"""
        try:
            print("ℹ️  Downloading all categories...")

            categories = []
            page = 1

            # First request (to get number_of_pages)
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/categories', params=params)
            data = response.json()

            if response.status_code != 200:
                error_description = data.get('error_description', 'Unknown error')
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            number_of_pages = data['pages']
            page_data = data.get('list', [])
            categories.extend(page_data)

            # Initialize tqdm progress bar
            pbar = tqdm(total=number_of_pages, desc="Downloading category pages")
            pbar.update(1)

            # Continue fetching remaining pages
            for page in range(2, number_of_pages + 1):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/categories', params=params)
                data = response.json()

                if response.status_code != 200:
                    error_description = data.get('error_description', 'Unknown error')
                    print(f'❌ API Error: {error_description}')
                    pbar.close()
                    return {'success': False, 'error': error_description}

                page_data = data.get('list', [])
                categories.extend(page_data)
                pbar.update(1)

            pbar.close()
            df = pd.DataFrame(categories)
            return df

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
    
    def get_all_categories_json(self):
        """Get all categories from Shoper and return them as a dict of category_id -> category"""
        try:
            print("ℹ️  Downloading all categories...")

            categories = []
            page = 1

            # First request to get the number of pages
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/categories', params=params)
            data = response.json()

            if response.status_code != 200:
                error_description = data.get('error_description', 'Unknown error')
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            number_of_pages = data['pages']
            page_data = data.get('list', [])
            categories.extend(page_data)

            # Initialize tqdm
            pbar = tqdm(total=number_of_pages, desc="Downloading category pages")
            pbar.update(1)

            # Remaining pages
            for page in range(2, number_of_pages + 1):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/categories', params=params)
                data = response.json()

                if response.status_code != 200:
                    error_description = data.get('error_description', 'Unknown error')
                    print(f'❌ API Error: {error_description}')
                    pbar.close()
                    return {'success': False, 'error': error_description}

                page_data = data.get('list', [])
                categories.extend(page_data)
                pbar.update(1)

            pbar.close()

            # Convert to dict using category_id as key
            categories_dict = {category['category_id']: category for category in categories}
            return categories_dict

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)

        