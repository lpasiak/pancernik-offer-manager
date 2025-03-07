from ..shoper_connect import ShoperAPIClient
from .pictures import ShoperPictures
import config, json
import pandas as pd

class ShoperProducts:
    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client
        self.pictures = ShoperPictures(client)

    def create_product(self, product_data):
        """Create a new product in Shoper
        Args:
            product_data (dict): Product data
        Returns:
            product_id (int)|None: Product id if successful, None if failed
        """
        try:
            response = self.client._handle_request('POST', f'{self.client.site_url}/webapi/rest/products', json=product_data)
            response_data = response.json()  # Could raise JSONDecodeError
            
            if response.status_code == 200:
                print(f'✅ Product {response_data["product_id"]} created successfully')
                return response_data
                
            # Handle "successful" requests that failed for business reasons
            print(f'❌ API Error: {response.status_code}, {response.text}')
            return None
            
        except Exception as e:
            # Handle network errors, JSON parsing errors, etc.
            print(f'❌ Request failed: {str(e)}')
            return None

    # TO BE REBUILT in the future, so a user will also be able to remove a product by SKU
    def remove_product(self, product_id):
        """Remove a product from Shoper
        Args:
            product_id (int): Product id
        Returns:
            True|None: True if successful, None if failed
        """
        try:
            response = self.client._handle_request('DELETE', f'{self.client.site_url}/webapi/rest/products/{product_id}')
            
            if response.status_code == 200:
                print(f'✅ Product {product_id} removed successfully')
                return True
                
            print(f'❌ API Error: {response.status_code}, {response.text}')
            return None
            
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return None
        
    def update_product(self, product_id, **kwargs):
        pass

    def get_a_product_by_code(self, identifier, pictures=False, use_code=False):
        """Get a product from Shoper by either product ID or product code.
        Args:
            identifier (int|str): Product ID (int) or product code (str)
            use_code (bool): If True, use product code (SKU) instead of ID
        Returns:
            dict|None: Product data if successful, None if failed
        """
        try:
            if use_code:
                # Get product by product code (SKU)
                product_filter = {
                    "filters": json.dumps({"stock.code": identifier})
                }
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products', params=product_filter)
                product_list = response.json().get('list', [])

                if not product_list:
                    print(f'❌ Product {identifier} doesn\'t exist')
                    return None

                product = product_list[0]
                
            else:
                # Get product by product ID
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products/{identifier}')
                product = response.json()
                
                if response.status_code != 200:
                    print(f'❌ API Error: {response.status_code}, {response.text}')
                    return None

            # Get product pictures if requested
            if pictures:
                try:
                    product['img'] = self.pictures.get_product_pictures(product['product_id'])
                except Exception as e:
                    print(f'❌ Error fetching product images: {str(e)}')
                    # Continue without images if they fail to fetch

            print(f'✅ Product {identifier} fetched successfully')
            return product

        except Exception as e:
            print(f'❌ Error fetching product {identifier}: {str(e)}')
            return None

    # TO BE REBUILT in the future, so a user will be able to filter products
    def get_all_products(self):
        """Get all products from Shoper and return them as df or None and save to Excel."""
        try:
            print("Downloading all products...")

            products = []
            page = 1
            
            while True:
                params = {'limit': config.SHOPER_LIMIT, 'page': page}
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products', params=params)
                data = response.json()
                number_of_pages = data['pages']

                if response.status_code != 200:
                    print(f'❌ API Error: {response.status_code}, {response.text}')
                    return None
                    
                page_data = data.get('list', [])
                
                if not page_data:
                    break
                    
                print(f'Page: {page}/{number_of_pages}')
                products.extend(page_data)
                page += 1
                
            df = pd.DataFrame(products)
            df.to_excel(config.SHEETS_DIR / 'shoper_all_products.xlsx', index=False)
            return df
            
        except Exception as e:
            print(f'❌ Error fetching all products: {str(e)}')
            return None