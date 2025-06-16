import config, json
from utils.logger import get_outlet_logger


class ShoperPictures:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.outlet_logger = get_outlet_logger().get_logger()

    def get_product_pictures(self, product_id):
        """Get product images from Shoper
        Args:
            product_id (int): Product code
        Returns:
            list|None: List of product images if successful, None if failed
        """
        photo_filter = {
            "filters": json.dumps({"product_id": product_id}),
            "limit": config.SHOPER_LIMIT
        }

        try:
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/product-images', params=photo_filter)
            
            if response.status_code != 200:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                self.outlet_logger.critical(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}
                
            return response.json()['list']
        
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.critical(f'❌ Request failed: {str(e)}')
            return str(e)
        
    def update_product_image(self, image_data):
        """Update product image
        Args:
            image_data (dict): Image data
        Returns:
            dict|None: Image data if successful, None if failed
        """
        try:
            response = self.client._handle_request('POST', f'{self.client.site_url}/webapi/rest/product-images/', json=image_data)
            
            if response.status_code != 200:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                self.outlet_logger.critical(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}
            
            return response
        
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            self.outlet_logger.critical(f'❌ Request failed: {str(e)}')
            return str(e)

    def change_product_picture(self, photo_id, new_url):
        """Changes a photo to a new one
        Args:
            photo_id (int): Photo id
            photo_url (str): Full photo url
        """
        photo_name = new_url.split('/')[-1]

        params = {
            'url': new_url,
            'translations': {'pl_PL': {'name': photo_name}}
        }
        response = self.client._handle_request('PUT', f'{self.client.site_url}/webapi/rest/product-images/{photo_id}', json=params)

        return response.json()
       