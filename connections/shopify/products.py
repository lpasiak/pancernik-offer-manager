import shopify
import config, json
import pandas as pd

class ShopifyProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client