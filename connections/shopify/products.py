import shopify
import json
import config
import pandas as pd


class ShopifyProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.query_product_light = config.query_product_light
        self.query_product_bizon = config.query_product_bizon
        
    def get_all_products_light(self):
        """Get all products from Shopify and return them as JSON or None."""
        try:
            all_products = []
            has_next_page = True
            cursor = None
            
            while has_next_page:
                current_query = self.query_product_light.replace(
                    'after: null',
                    f'after: "{cursor}"' if cursor else 'after: null'
                )
                
                result = shopify.GraphQL().execute(current_query)
                result = json.loads(result)
                
                products_data = result['data']['products']
                for edge in products_data['edges']:
                    product = edge['node']
                    # Extract variants into a simpler list
                    product['variants'] = [
                        variant['node'] 
                        for variant in product['variants']['edges']
                    ]
                    all_products.append(product)
                
                has_next_page = products_data['pageInfo']['hasNextPage']
                cursor = products_data['pageInfo']['endCursor']
                
                print(f"Fetched {len(all_products)} products so far...")
            
            return all_products

        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return str(e)
        
    def get_all_products_bizon(self):
        """Get all products from Shopify and return them as JSON or None."""
        try:
            all_products = []
            has_next_page = True
            cursor = None
            
            while has_next_page:
                current_query = self.query_product_bizon.replace(
                    'after: null',
                    f'after: "{cursor}"' if cursor else 'after: null'
                )
                
                result = shopify.GraphQL().execute(current_query)
                result = json.loads(result)
                
                products_data = result['data']['products']
                for edge in products_data['edges']:
                    product = edge['node']
                    # Extract variants into a simpler list
                    product['variants'] = [
                        variant['node'] 
                        for variant in product['variants']['edges']
                    ]
                    all_products.append(product)
                
                has_next_page = products_data['pageInfo']['hasNextPage']
                cursor = products_data['pageInfo']['endCursor']
                
                print(f"Fetched {len(all_products)} Bizon products so far...")
            
            return all_products

        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return str(e)

    def update_products_urls(self):
        """Update a product in Shopify"""

        products = pd.read_csv(f'{config.SHEETS_DIR}/handles-bizon.csv', delimiter=';')

        product_dict = {}

        for _, row in products.iterrows():
            product_dict[row['id']] = row['handle']

        for id, handle in product_dict.items():
            mutation = config.mutation_product_update_url(product_id=id, new_url=handle)

            result = shopify.GraphQL().execute(mutation)
            result = json.loads(result)
            
            response_data = result.get('data', {}).get('productUpdate', {})
            updated_product = response_data.get('product', {})
            errors = response_data.get('userErrors', [])
            
            if errors:
                print("❌ Errors occurred during update:")
                for error in errors:
                    print(f"- Field: {error.get('field')}, Message: {error.get('message')}")
                return None
                
            print(f"✅ Product {updated_product.get('id')} updated successfully!")
            print(f"New handle: {updated_product.get('handle')}")
