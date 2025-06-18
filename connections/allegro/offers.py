import config
import json
from tqdm import tqdm


class AllegroOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_an_offer_by_id(self, identifier):
        url = f'{config.ALLEGRO_API_URL}/sale/product-offers/{identifier}'
        response = self.client.session.request('GET', url)

        return response.json()

    def get_all_offers(self):
        url = f'{config.ALLEGRO_API_URL}/sale/offers'

        all_offers = []

        product_limit = 100
        offset = 0

        params = {'limit': product_limit, 'offset': offset}
        response = self.client.session.request('GET', url, params=params)
        data = response.json()
        total_products = data.get('totalCount', 0)

        print(f"Total offers available: {total_products}")

        for offset in tqdm(range(0, total_products, product_limit), desc="Downloading offers", unit=" product"):
            params = {'limit': product_limit, 'offset': offset}
            response = self.client.session.request('GET', url, params=params)
            data = response.json()
            offers = data.get('offers', [])

            if not offers:
                break

            all_offers.extend(offers)

        with open('allegro.json', 'w', encoding='utf-8') as f:
            json.dump(all_offers, f, indent=2)

        return all_offers

    def get_an_offer_by_id(self, offer_id):
        url = f'{config.ALLEGRO_API_URL}/sale/product-offers/{offer_id}'

        response = self.client.session.request('GET', url)

        print(response)

