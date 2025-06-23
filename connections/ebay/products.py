import config
import requests


class EbayProducts:
    def __init__(self, client):
        self.client = client

    def get_product_listing(self, limit=1, offset=0):
        try:
            endpoint = "https://api.ebay.com/sell/inventory/v1/inventory_item"
            params = {
                "limit": limit,
                "offset": offset
            }

            response = self.client.session.get(endpoint, params=params)
            print(response.text)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error in eBay get_product_listing: {e}')