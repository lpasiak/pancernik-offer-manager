import config
from utils.logger import get_outlet_logger


class ShoperRedirects:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.outlet_logger = get_outlet_logger()

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
            redirect_id = response.json()

            if response.status_code == 200:
                print(f'✅ Redirect {redirect_id} created')
                self.outlet_logger.info(f'✅ Redirect {redirect_id} created')
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
                print(f'✅ Redirect {identifier} removed successfully.')
                self.outlet_logger.info(f'✅ Redirect {identifier} removed successfully.')
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
