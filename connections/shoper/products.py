from ..shoper_connect import ShoperAPIClient
import config
import pandas as pd
import json

class ShoperProducts:
    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client

    def create_product(self, product_data):
        """Create a new product in Shoper
        Args:
            product_data (dict): Product data
        """
        response = self.client._handle_request('POST', f'{self.client.site_url}/webapi/rest/products', json=product_data)

        if response.status_code == 200:
            print(f'✅ Product {response.json()["product_id"]} created successfully')
        else:
            print(f'❌ Error creating product {response.json()["product_id"]}: {response.status_code}, {response.text}')

        return response.json()

    def remove_product(self, product_id):
        """Remove a product from Shoper
        Args:
            product_id (int): Product id"""
        response = self.client._handle_request('DELETE', f'{self.client.site.url}/webapi/rest/products/{product_id}')

        if response.status_code == 200:
            print(f'✅ Product {product_id} removed successfully')
        else:
            print(f'❌ Error removing product {product_id}: {response.status_code}, {response.text}')

        return response.json()

    def get_a_single_product(self, product_id):
        """Get a product from Shoper by product id
        Args:
            product_id (int): Product id"""
        response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products/{product_id}')

        if response.status_code == 200:
            print(f'✅ Product {product_id} fetched successfully')
        else:
            print(f'❌ Error fetching product {product_id}: {response.status_code}, {response.text}')

        return response.json()

    def get_a_single_product_by_code(self, product_code):
        """Get a product from Shoper by product code and return a product json.
        Args:
            product_code (str): Product code"""
        product_filter = {
            "filters": json.dumps({"stock.code": product_code})
        }
        
        response = self._handle_request('GET', f'{self.client.site_url}/webapi/rest/products', params=product_filter)
        product_list = response.json().get('list', [])
            
        if not product_list:
            print(f'❌ | Product {product_code} doesn\'t exist')
            return None
            
        return product_list[0]
    
    # TO DO: CONTINUE HERE
    def get_a_single_product_by_code_with_pictures(self, product_code):
        """Get a product from Shoper by product code and return a product json with images included.
        Args:
            product_code (str): Product code"""

        product_filter = {
            "filters": json.dumps({"stock.code": product_code})
        }

        try:
            response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products', params=product_filter)
            product_list = response.json().get('list', [])
            
            if not product_list:
                print(f'Product {product_code} doesn\'t exist')
                return None
            
            product = product_list[0]
            product_id = product['product_id']

            photo_filter = {
                "filters": json.dumps({"product_id": product_id}),
                "limit": 50
            }

            photo_response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/product-images', params=photo_filter)
            product_photos = photo_response.json()['list']
            product['img'] = product_photos

            return product
        
        except Exception as e:
            print(f'Error fetching product {product_code}: {str(e)}')
            return None
        
    def get_all_products(self):
        """Get all products from Shoper, return them as a DataFrame and save to Excel."""
        products = []
        page = 1
        url = f'{self.client.site_url}/webapi/rest/products'

        print("Downloading all products.")
        while True: 
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                break

            print(f'Page: {page}/{number_of_pages}')
            products.extend(page_data)
            page += 1

        df = pd.DataFrame(products)
        df.to_excel(config.ROOT_DIR / 'shoper_all_products.xlsx', index=False)

        return df