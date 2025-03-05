import requests, time
from pathlib import Path
import config

class ShoperAPIClient:

    def __init__(self, site_url, login, password):

        self.site_url = site_url
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.token = None

        self.sheets_dir = Path('sheets')
        self.sheets_dir.mkdir(exist_ok=True)
        
    def _handle_request(self, method, url, **kwargs):
        """Handle API requests with automatic retry on 429 errors."""
        while True:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get('Retry-After', 1))
                time.sleep(retry_after)
            else:
                return response
            
    def connect(self):
        """Authenticate with the API"""
        response = self._handle_request(
            'POST',
            f'{self.site_url}/webapi/rest/auth',
            auth=(self.login, self.password)
        )

        if response.status_code == 200:
            self.token = response.json().get('access_token')
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            print(f"Shoper Authentication {config.SITE} successful.")
        else:
            raise Exception(f"Authentication failed: {response.status_code}, {response.text}")


