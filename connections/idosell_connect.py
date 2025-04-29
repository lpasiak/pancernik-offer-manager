import requests
import config


class IdoSellAPIClient:

    def __init__(self, api_key):

        self.api_key = api_key
        self.session = requests.Session()

    def connect(self):
        """Authenticate with the API"""
        self.session.headers.update({'X-API-KEY': self.api_key})

