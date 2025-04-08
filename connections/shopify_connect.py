import requests, time
from pathlib import Path
import config
import shopify

class ShopifyAPIClient:

    def __init__(self, shop_url, api_version, api_token):

        self.shop_url = shop_url
        self.api_version = api_version
        self.api_token = api_token
        self.session = shopify.Session(self.shop_url, self.api_version, self.api_token)

    def connect(self):
        shopify.ShopifyResource.activate_session(self.session)
        
        
