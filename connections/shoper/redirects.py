import config
from utils.logger import get_outlet_logger
from tqdm import tqdm
import pandas as pd


class ShoperRedirects:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.outlet_logger = get_outlet_logger().get_logger()

    def get_all_redirects(self):
        """Get all redirects from Shoper and return them as df or None"""

        try:
            print("ℹ️  Downloading all redirects...")
            url = f'{config.SHOPER_SITE_URL}/webapi/rest/redirects'

            redirects = []

            # First request to determine number of pages
            initial_params = {'limit': config.SHOPER_LIMIT, 'page': 1}
            initial_response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/redirects', params=initial_params)
            
            if initial_response.status_code != 200:
                error_description = initial_response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                self.outlet_logger.warning(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

            initial_data = initial_response.json()
            number_of_pages = initial_data['pages']
            redirects.extend(initial_data.get('list', []))

            # Use tqdm for the rest of the pages
            for page in tqdm(range(2, number_of_pages + 1), desc="Downloading pages", unit=" page"):
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/redirects', params=params)

                if response.status_code != 200:
                    print(f"❌ Error on page {page}: {response.status_code}")
                    self.outlet_logger.warning(f"❌ Error on page {page}: {response.status_code}")
                    continue

                page_data = response.json().get('list', [])
                if not page_data:
                    return None

                redirects.extend(page_data)

            df = pd.DataFrame(redirects)
            return df
        
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)
        
    def create_redirect(self, redirect_data):
        """Create a redirect for a product.
        Args:
            redirect_data (dict): Data about the discount:
                redirected_url: string
                target_url: string

        Returns:
            Redirect id if succesful, False if failed
        """
        try:

            params = {
                'route': redirect_data['redirected_url'],
                'type': 0,
                'target': redirect_data['target_url'],
            }
            
            url = f'{config.SHOPER_SITE_URL}/webapi/rest/redirects'

            response = self.client._handle_request('POST', url, json=params)

            if response.status_code == 200:
                return response.json()
            else:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                self.outlet_logger.warning(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}
            
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)

    def remove_redirect(self, identifier):
        """Remove a redirect
        Args:
            identifier (int|str): Redirect id
        Returns:
            bool: True if succesful, False if failed
        """

        try:
            url = f'{config.SHOPER_SITE_URL}/webapi/rest/redirects/{identifier}'
            response = self.client._handle_request('DELETE', url)

            if response.status_code == 200:
                return True
            else:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                self.outlet_logger.warning(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}
                    
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.warning(f'❌ Request failed: {str(e)}')
            return str(e)
