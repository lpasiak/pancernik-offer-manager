import config
import pandas as pd
from tqdm import tqdm


class ShoperProducers:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_producers(self):
        """Get all producers from Shoper and return them as df or None"""
        try:
            print("ℹ️  Downloading all producers...")

            producers = []
            page = 1

            # First request (to get number_of_pages)
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/producers', params=params)
            data = response.json()

            if response.status_code != 200:
                error_description = data.get('error_description', 'Unknown error')
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            number_of_pages = data['pages']
            page_data = data.get('list', [])
            producers.extend(page_data)

            # Initialize tqdm progress bar
            pbar = tqdm(total=number_of_pages, desc="Downloading producers", unit=' page')
            pbar.update(1)

            # Continue fetching remaining pages
            for page in range(2, number_of_pages + 1):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/producers', params=params)
                data = response.json()

                if response.status_code != 200:
                    error_description = data.get('error_description', 'Unknown error')
                    print(f'❌ API Error: {error_description}')
                    pbar.close()
                    return {'success': False, 'error': error_description}

                page_data = data.get('list', [])
                producers.extend(page_data)
                pbar.update(1)

            pbar.close()
            df = pd.DataFrame(producers)
            return df

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
    
    def get_all_producers_json(self):
        """Get all producers from Shoper and return them as a dict of producer_id -> producer"""
        try:
            print("ℹ️  Downloading all producers...")

            producers = []
            page = 1

            # First request to get the number of pages
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/producers', params=params)
            data = response.json()

            if response.status_code != 200:
                error_description = data.get('error_description', 'Unknown error')
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            number_of_pages = data['pages']
            page_data = data.get('list', [])
            producers.extend(page_data)

            # Initialize tqdm
            pbar = tqdm(total=number_of_pages, desc="Downloading producers", unit=' page')
            pbar.update(1)

            # Remaining pages
            for page in range(2, number_of_pages + 1):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/producers', params=params)
                data = response.json()

                if response.status_code != 200:
                    error_description = data.get('error_description', 'Unknown error')
                    print(f'❌ API Error: {error_description}')
                    pbar.close()
                    return {'success': False, 'error': error_description}

                page_data = data.get('list', [])
                producers.extend(page_data)
                pbar.update(1)

            pbar.close()

            # Convert to dict using producer_id as key
            producers_dict = {producer['producer_id']: producer for producer in producers}
            return producers_dict

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)

        