import requests
import config


class IdoSellAPIClient:

    def __init__(self, api_key, site):

        self.api_key = api_key
        self.site = site
        self.session = requests.Session()

    def connect(self):
        """Authenticate with the API"""
        self.session.headers.update({'X-API-KEY': self.api_key})

