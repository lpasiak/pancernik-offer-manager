import requests
import config
import json

class IdoSellProducts:
    def __init__(self, client):
        """Initialize an IdoSell Client"""
        self.client = client

    def get_all_products(self):
        """Get all products from IdoSell and return them as JSON."""

        try:
            url = f"{self.client.site}/api/admin/v5/products/products/search"
            all_data = []
            page = 0

            payload = {
                'params': {
                    "returnProducts": "active", 
                    "returnElements": ["code", "sizes_attributes"],
                    "resultsLimit": 100,
                    "resultsPage": 0
                }
            }

            response = self.client.session.request('POST', url, json=payload)
            data = response.json()
            number_of_pages = data['resultsNumberPage']

            for page in range(number_of_pages):
                payload['params']['resultsPage'] = page

                response = self.client.session.request('POST', url, json=payload)
                data = response.json()['results']
                print(f"{page + 1}/{number_of_pages}")

                transformed_data = []

                for product in data:
                    transformed_product = {
                        'product_id': product['productId'],
                        'product_code': product['productDisplayedCode'],
                        'product_external_code': product['productSizesAttributes'][0]['productSizeCodeExternal']
                    }
                    transformed_data.append(transformed_product)

                all_data.append(transformed_data)

            return all_data

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
        
    def add_stock_price(self, price, external_code):
        """Add """
        try:
            payload = { "params": { "products": [
                {
                    "productPurchasePrice": price,
                    "productSizeCodeExternal": external_code
                } ] } }
            
            url = f"{self.client.site}/api/admin/{config.IDOSELL_API_VERSION}/products/stockQuantity"
            response = self.client.session.request('PUT', url, json=payload)

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)