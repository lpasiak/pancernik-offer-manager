from .pictures import ShoperPictures
import config, json
import pandas as pd

class ShoperProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.pictures = ShoperPictures(client)

    def get_product_by_code(self, identifier, pictures=False, use_code=False):
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
                    return {'success': False, 'error': f'❌ Product {identifier} doesn\'t exist'}

                product = product_list[0]
                
            else:
                # Get product by product ID
                response = self.client._handle_request('GET', f'{self.client.site_url}/webapi/rest/products/{identifier}')
                product = response.json()
                
                if response.status_code != 200:
                    error_description = response.json()['error_description']
                    print(f'❌ API Error: {error_description}')
                    return {'success': False, 'error': error_description}

            # Get product pictures if requested
            if pictures:
                try:
                    product['img'] = self.pictures.get_product_pictures(product['product_id'])
                except Exception as e:
                    print(f'❌ Error fetching product images: {str(e)}')
                    # Continue without images if they fail to fetch

            return product

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
        
    def create_product(self, product_data):
        """Create a new product in Shoper
        Args:
            product_data (dict): Product data
        Returns:
            int|None: Product ID if successful, None if failed
        """
        try:
            response = self.client._handle_request('POST', f'{self.client.site_url}/webapi/rest/products', json=product_data)
            
            if response.status_code == 200:
                try:
                    product_id = response.json()
                    if isinstance(product_id, int):
                        print(f'✅ Product {product_id} | {product_data["code"]} created successfully')
                        return product_id
                    else:
                        print(f'❌ Unexpected response format: {product_id}')
                        return None
                except ValueError as e:
                    print(f'❌ Invalid response format: {str(e)}')
                    return None
                
            error_description = response.json()['error_description']
            print(f'❌ API Error: {error_description}')
            return {'success': False, 'error': error_description}
            
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)

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
                
            error_description = response.json()['error_description']
            print(f'❌ API Error: {error_description}')
            return {'success': False, 'error': error_description}
            
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
        
    def update_product_by_code(self, identifier, use_code=False, **parameters):
        """Update a product from Shoper. Returns True if successful, None if failed
        Args:
            identifier (int|str): Product id or product code
            use_code (bool): If True, use product code (SKU) instead of ID
            parameters key=value: Parameters to update
        Returns:
            True|None: True if successful, None if failed
        """

        try:
            if use_code:
                # Get product id by product code (SKU)
                product = self.get_product_by_code(identifier, use_code=True)
                product_id = product['product_id']
            else:
                product_id = identifier

            params = {}

            for key, value in parameters.items():
                if value is not None:
                    params[key] = value
            response = self.client._handle_request('PUT', f'{self.client.site_url}/webapi/rest/products/{product_id}', json=params)

            if response.status_code == 200:
                print(f'✅ Product {product_id} updated successfully with {list(parameters.keys())}')
                return True
                
            error_description = response.json()['error_description']
            print(f'❌ API Error: {error_description}')
            return {'success': False, 'error': error_description}
        
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)

    # TO BE REBUILT in the future, so a user will be able to filter products
    def get_all_products(self):
        """Get all products from Shoper and return them as df or None."""
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
                    error_description = response.json()['error_description']
                    print(f'❌ API Error: {error_description}')
                    return {'success': False, 'error': error_description}
                    
                page_data = data.get('list', [])
                
                if not page_data:
                    break
                    
                print(f'Page: {page}/{number_of_pages}')
                products.extend(page_data)
                page += 1

            df = pd.DataFrame(products)
            return df
            
        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)