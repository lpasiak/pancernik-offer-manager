import requests
import config


class EbayAPIClient:

    def __init__(self, ebay_token):
        self.token = ebay_token
        self.session = requests.Session()

    def connect(self):
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})

