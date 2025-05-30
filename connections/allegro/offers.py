import config


class AllegroOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_an_offer_by_id(self, identifier):
        url = f'{config.ALLEGRO_API_URL}/sale/product-offers/{identifier}'
        response = self.client.session.request('GET', url)

        return response.json()
