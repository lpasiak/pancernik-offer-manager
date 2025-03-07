from ..shoper_connect import ShoperAPIClient
import config, os
import pandas as pd

class ShoperAttributes:

    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client

        