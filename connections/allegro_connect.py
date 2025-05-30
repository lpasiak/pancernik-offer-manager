import requests
import base64
import time
import json
import os
from datetime import datetime, timedelta, timezone
import config


class AllegroAPIClient:
    def __init__(self):
        self.token_manager = AllegroTokenManager(
            client_id=config.ALLEGRO_CLIENT_ID,
            client_secret=config.ALLEGRO_API_SECRET,
            api_url=config.ALLEGRO_API_URL,
        )
        self.token = self.token_manager.get_access_token()
        self.session = requests.Session()
        self.site = config.ALLEGRO_SITE

    def connect(self):
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Accept': config.ALLEGRO_API_VERSION
        })


class AllegroTokenManager:
    def __init__(self, client_id, client_secret, api_url, token_file=f'{config.ROOT_DIR}/credentials/allegro_{config.ALLEGRO_SITE.lower()}_token.json'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = api_url
        self.code_url = f'{self.api_url}/auth/oauth/device'.replace("api.", "")
        self.token_url = f'{self.api_url}/auth/oauth/token'.replace("api.", "")
        self.token_file = token_file
        self.token_data = self.load_tokens()

    def get_basic_auth_header(self):
        credentials = f'{self.client_id}:{self.client_secret}'
        b64 = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {b64}'}

    def save_tokens(self, data):
        data['expires_at'] = (datetime.now(timezone.utc) + timedelta(seconds=int(data['expires_in']))).timestamp()
        with open(self.token_file, 'w') as f:
            json.dump(data, f, indent=2)
        self.token_data = data

    def load_tokens(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None

    def is_token_valid(self):
        if not self.token_data:
            return False
        expires_at = datetime.fromtimestamp(self.token_data.get('expires_at', 0), tz=timezone.utc)
        return expires_at > datetime.now(timezone.utc)

    def refresh_access_token(self):
        if not self.token_data or 'refresh_token' not in self.token_data:
            return None

        headers = {
            **self.get_basic_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.token_data['refresh_token']
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        if response.status_code == 200:
            tokens = response.json()
            self.save_tokens(tokens)
            return tokens['access_token']
        else:
            print('Refresh failed:', response.text)
            return None

    def start_device_flow(self):
        headers = {
            **self.get_basic_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'client_id': self.client_id}
        response = requests.post(self.code_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            print('❌ Failed to start device flow:', response.status_code, response.text)
            raise Exception('Could not start device flow')

    def poll_for_token(self, device_code, interval):
        headers = {
            **self.get_basic_auth_header(),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code
        }

        while True:
            time.sleep(interval)
            response = requests.post(self.token_url, headers=headers, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.save_tokens(token_data)
                return token_data['access_token']

            error = response.json().get('error')
            if error == 'authorization_pending':
                continue
            elif error == 'slow_down':
                interval += interval
            else:
                raise Exception(f'Authorization failed: {response.text}')

    def authenticate(self):
        code_data = self.start_device_flow()
        print('Open this URL and enter code:')
        print(code_data['verification_uri_complete'])
        return self.poll_for_token(code_data['device_code'], int(code_data['interval']))

    def get_access_token(self):
        if self.is_token_valid():
            return self.token_data['access_token']

        if 'sandbox' in self.api_url:
            print('Sandbox does not support token refresh. Falling back to manual login.')
            return self.authenticate()
        
        print('Token expired or missing. Attempting to refresh...')
        new_token = self.refresh_access_token()
        if new_token:
            return new_token

        print('Manual login required.')
        return self.authenticate()
