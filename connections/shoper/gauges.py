import config
import pandas as pd
from tqdm import tqdm


class ShoperGauges:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_gauges(self):
        """Get all gauges from Shoper. Returns a pandas DataFrame if successful, None if failed"""
        gauges = []
        page = 1
        url = f'{self.client.site_url}/webapi/rest/gauges'

        print("ℹ️  Downloading all gauges...")
        while True:
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                break

            print(f'Page: {page}/{number_of_pages}')
            gauges.extend(page_data)
            page += 1

        df = pd.DataFrame(gauges)
        return df
    
    def get_all_gauges_json(self):
        """Get all gauges from Shoper."""
        try:
            print("ℹ️  Downloading all gauges...")

            # First request to get total number of pages
            initial_params = {'limit': config.SHOPER_LIMIT, 'page': 1}
            initial_response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/gauges', params=initial_params)
            if initial_response.status_code != 200:
                error_description = initial_response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            initial_data = initial_response.json()
            number_of_pages = initial_data['pages']
            gauges = initial_data.get('list', [])

            # Use tqdm for the rest of the pages
            for page in tqdm(range(2, number_of_pages + 1), desc="Downloading pages", unit=" page"):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/gauges', params=params)
                
                if response.status_code != 200:
                    print(f"❌ Error on page {page}: {response.status_code}")
                    continue

                page_data = response.json().get('list', [])
                if not page_data:
                    break

                gauges.extend(page_data)
            return gauges

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)