import config
import requests


class EbayProducts:
    def __init__(self, client):
        self.client = client

    def get_product_listing(self):
        response = self.client.session.request('GET', 
                                               'https://api.sandbox.ebay.com/sell/inventory/v1/inventory_item?limit=2&offset=0'

        )
        print(response)
        print(response.text)
        print(response.json)
