import shopify
import json
import config

class ShopifyProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.query_product_download = config.query_product_download
        
    def get_all_products(self):
        """Get all products from Shopify and return them as JSON or None."""
        try:
            all_products = []
            has_next_page = True
            cursor = None
            
            while has_next_page:
                current_query = self.query_product_download.replace(
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

    def update_a_product(self):
        """Update a product in Shopify"""
        mutation = config.get_product_update_mutation(product_id='gid://shopify/Product/839310392', new_title='Test Product')

        result = shopify.GraphQL().execute(mutation)
        result = json.loads(result)
        print(result)
