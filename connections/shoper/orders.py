import config
import pandas as pd
from tqdm import tqdm


class ShoperCategories:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client