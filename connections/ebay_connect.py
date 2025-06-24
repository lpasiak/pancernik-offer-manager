import base64
import json
import os
import time
import urllib.parse
import webbrowser
import requests
import config

# Different APIs use different Authentication methods. 
# EbayAPIClient is built with RESTful InventoryAPI in mind, 
# whereas there are still eBay APIs that use older authentication
# methods - e.g. TradingAPI :((


class EbayTradingAPIClient:
    def __init__(self):
        pass




class EbayAPIClient:
    def __init__(self):
        self.oauth = None
        self.token = None
        self.session = requests.Session()

    def connect(self):
        self.oauth = EbayOAuthTokenClient(
            client_id=config.EBAY_CLIENT_ID,
            client_secret=config.EBAY_CLIENT_SECRET,
            redirect_uri=config.EBAY_REDIRECT_URI
        )
        self.oauth.authenticate()
        self.token = self.oauth.access_token
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        })


class EbayOAuthTokenClient:
    AUTH_URL = 'https://auth.ebay.com/oauth2/authorize'
    TOKEN_URL = 'https://api.ebay.com/identity/v1/oauth2/token'
    API_SCOPE = 'https://api.ebay.com/oauth/api_scope/sell.inventory'
    TOKEN_FILE = f'{config.ROOT_DIR}/credentials/ebay_token.json'

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None

    def get_authorization_url(self):
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.API_SCOPE
        }
        return f'{self.AUTH_URL}?{urllib.parse.urlencode(params)}'

    def open_authorization_url(self):
        url = self.get_authorization_url()
        print('Open this URL in your browser and log in:')
        print(url)
        webbrowser.open(url)

    def exchange_code_for_token(self, auth_code):
        credentials = f'{self.client_id}:{self.client_secret}'
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded}'
        }

        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        print(response.text)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data['access_token']
        self.refresh_token = token_data.get('refresh_token')

        if not self.refresh_token:
            print("Warning: No refresh_token received. You will have to re-authenticate manually after the token expires.")

        self.save_tokens(token_data)
        return token_data

    def refresh_access_token(self):
        credentials = f'{self.client_id}:{self.client_secret}'
        encoded = base64.b64encode(credentials.encode()).decode()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded}'
        }

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'scope': self.API_SCOPE
        }

        response = requests.post(self.TOKEN_URL, headers=headers, data=data)
        print('Refresh response:', response.status_code)
        print(response.text)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data['access_token']
        self.refresh_token = token_data.get('refresh_token', self.refresh_token)
        self.save_tokens(token_data)
        return token_data

    def save_tokens(self, token_data):
        token_data['timestamp'] = int(time.time())
        with open(self.TOKEN_FILE, 'w') as f:
            json.dump(token_data, f)

    def load_tokens(self):
        if not os.path.exists(self.TOKEN_FILE):
            return None
        with open(self.TOKEN_FILE, 'r') as f:
            return json.load(f)

    def is_token_expired(self, token_data):
        expires_in = token_data.get('expires_in', 7200)
        timestamp = token_data.get('timestamp', 0)
        return (time.time() - timestamp) >= (expires_in - 60)

    def authenticate(self):
        token_data = self.load_tokens()
        if token_data:
            self.access_token = token_data['access_token']
            self.refresh_token = token_data.get('refresh_token', 0)
            if self.is_token_expired(token_data):
                if self.refresh_token == 0:
                    print('Access token expired. Refreshing...')
                    self.refresh_access_token()
                else:
                    print('Access token expired and no refresh token available. Manual re-authentication required.')
                    self.manual_auth_flow()

        else:
            print('No saved token. Manual authorization required.')
            self.manual_auth_flow()

    def manual_auth_flow(self):
        self.open_authorization_url()
        raw_code = input('Paste your auth code from the URL: ')
        auth_code = urllib.parse.unquote(raw_code)
        self.exchange_code_for_token(auth_code)
