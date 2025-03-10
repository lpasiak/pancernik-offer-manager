from ..shoper_connect import ShoperAPIClient
import config, json

class ShoperPictures:

    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client

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
                print(f'❌ API Error: {response.status_code}, {response.text}')
                return None
                
            return response.json()['list']
        
        except Exception as e:
            print(f'❌ | Error fetching product images for {product_id}: {str(e)}')
            return None