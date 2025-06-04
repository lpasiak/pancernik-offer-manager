import requests
import urllib3
import config
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SubiektClient:

    def __init__(self, credentials):
        self.credentials = credentials
        self.session = requests.Session()
        self.token = None
        self.allowed_databases = None
        self.database_2025 = None
        self.database_2023 = None
        self.database_bizon = None

    def connect(self):
        auth_endpoint = f'{config.SUBIEKT_URL}/api/v1/authorization/authorize'
        response = self.session.request('POST', url=auth_endpoint, json=self.credentials, verify=False)

        if response.status_code == 200:
            self.token = response.json()['token']
            self.session.headers.update({
                'Authorization': f'Bearer {self.token}',
                'accept': 'application/json'
            })
        
        # Getting an account id
        allowed_databases_endpoint = f'{config.SUBIEKT_URL}/api/v1/configuration/allowed-databases'
        response = self.session.request('GET', url=allowed_databases_endpoint, verify=False)

        self.allowed_databases = response.json()
        self.database_2025 = self.allowed_databases[0]
        self.database_2023 = self.allowed_databases[1]
        self.database_bizon = self.allowed_databases[2]


    def get_products(self, database):
        products_endpoint = f'{config.SUBIEKT_URL}/api/v1/{database['name']}/products/'

        response = self.session.request('GET', url=products_endpoint, verify=False)
        data = response.json()

        with open('products.json', 'w') as f:
            json.dump(data, f, indent=4)

        return data
