import requests
import config
import json

class IdoSellProducts:
    def __init__(self, client):
        """Initialize an IdoSell Client"""
        self.client = client

    def get_all_products(self):
        """Get all products from IdoSell and return them as df or None."""

        try:
            print('Downloading all products')
            url = f"{self.client.site}/api/admin/{config.IDOSELL_API_VERSION}/products/products/search"

            response = self.client.session.request('POST', url)

            if response.status_code == 200:
                with open('xd.json', 'w', encoding='utf-8') as file:
                    product_data = response.json()['results']
                    json.dump(product_data, file, indent=2, sort_keys=True, ensure_ascii=False)
                return product_data
            
            else:
                error_description = response.json()['error_description']
                print(f'❌ API Error: {error_description}')
                return {'success': False, 'error': error_description}

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)