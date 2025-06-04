import config
import json


class SubiektProducts:
    def __init__(self, client):
        """Initialize a Subiekt Products"""
        self.client = client

    def get_products(self, database):
        products_endpoint = f'{config.SUBIEKT_URL}/api/v1/{database['name']}/products/'

        response = self.client.session.request('GET', url=products_endpoint, verify=False)
        data = response.json()

        with open('products.json', 'w') as f:
            json.dump(data, f, indent=4)

        return data