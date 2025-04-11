import shopify
import json
import pandas as pd
from . import ShopifyAPIClient
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
                all_products.extend([edge['node'] for edge in products_data['edges']])
                
                has_next_page = products_data['pageInfo']['hasNextPage']
                cursor = products_data['pageInfo']['endCursor']
                
                print(f"Fetched {len(all_products)} products so far...")
            
            return all_products

        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return str(e)

class ShopifyClient:
    def __init__(self):
        self.shopify_client = None
        self.shoper_products = None

    def connect(self):
        """Initialize connection with Shopify"""
        try:
            self.shopify_client = ShopifyAPIClient(
                shop_url=config.SHOPIFY_CREDENTIALS['shop_url'],
                api_version=config.SHOPIFY_API_VERSION,
                api_token=config.SHOPIFY_CREDENTIALS['api_token']
            )
            self.shopify_client.connect()
            self.shopify_products = ShopifyProducts(self.shopify_client)

            return True

        except Exception as e:
            print(f"Error initializing Shopify connections: {e}")
            return False