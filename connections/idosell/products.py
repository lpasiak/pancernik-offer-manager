import requests
import config
import json

class IdoSellProducts:
    def __init__(self, client):
        """Initialize an IdoSell Client"""
        self.client = client

    def get_all_product_codes(self):
        """Get all products' ids, codes and external codes from IdoSell and return them as JSON."""

        print('Downloading IdoSell offer codes...')
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

                for product in data:
                    transformed_product = {
                        'product_id': str(product['productId']),
                        'product_code': str(product['productDisplayedCode']),
                        'product_external_code': str(product['productSizesAttributes'][0]['productSizeCodeExternal'])
                    }
                    all_data.append(transformed_product)

            return all_data

        except Exception as e:
            print(f'❌ Request failed: {str(e)} | in get_all_product_codes')
            return str(e)
        
    def update_product_logistic_info(self, product_id, product_external_code, purchase_price_gross, weight, width, height, length):
        """Update products with Last Delivery Prices, Weights and Dimensions"""

        try:
            payload = { "params": {
                            "settings": { "settingModificationType": "edit" },
                            "products": [
                                {
                                    "productId": product_id,
                                    "productSizes": [
                                        {
                                            "productPurchasePriceGrossLast": purchase_price_gross,
                                            "productWeight": weight,
                                            "sizeId": "uniw",
                                            "productSizeCodeExternal": product_external_code
                                        }
                                    ],
                                    "productDimensions": {
                                        "productWidth": width / 10,
                                        "productHeight": height / 10,
                                        "productLength": length / 10
                                    }
                                }
                            ]
                        } }
            
            url = f'{self.client.site}/api/admin/{config.IDOSELL_API_VERSION}/products/products'
            response = self.client.session.request('PUT', url, json=payload)

            return response

        except Exception as e:
            print(f'❌ Request failed: {str(e)}')
            return str(e)
        