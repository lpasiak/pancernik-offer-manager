import pandas as pd
import requests
import urllib3
import config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class EasyStorageClient:

    def __init__(self, credentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.token = None
        self.pancernik_account_id = None
        self.bizon_account_id = None

    def connect(self):
        auth_endpoint = f'{config.EASYSTORAGE_URL}/api/v1/authorization/authorize'
        response = self.session.request('POST', url=auth_endpoint, json=self.credentials, verify=False)

        if response.status_code == 200:
            self.token = response.json()['token']
            self.session.headers.update({'Authorization': f'Bearer {self. token}'})

        # Getting an account id
        account_endpoint = f'{config.EASYSTORAGE_URL}/api/v1/accounts/'
        response = self.session.request(method='GET', url=account_endpoint, verify=False)

        self.pancernik_account_id = response.json()[1]['id']
        self.bizon_account_id = response.json()[0]['id']
