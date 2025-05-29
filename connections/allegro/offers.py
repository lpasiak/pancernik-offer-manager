import config, json
import pandas as pd
from tqdm import tqdm


class AllegroOffers:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_an_offer_by_id(self, identifier):
        url = f'{config.ALLEGRO_API_URL_SANDBOX}/sale/product-offers/{identifier}'
        response = self.client.session.get(url)

        return response.json()