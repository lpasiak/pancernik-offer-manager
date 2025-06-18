import config
import mimetypes
import json
from pathlib import Path
import requests


class AllegroProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
