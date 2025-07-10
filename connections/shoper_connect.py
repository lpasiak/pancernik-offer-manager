import requests, time
import config

class ShoperAPIClient:

    def __init__(self, site_url, login, password):

        self.site_url = site_url
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.token = None
        
    def _handle_request(self, method, url, max_retries=5, backoff_factor=1.5, **kwargs):
        """Handle API requests with automatic retry on 429 and 5xx errors."""
        attempt = 0

        while attempt < max_retries:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"429 Too Many Requests. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                attempt += 1
                continue

            elif response.status_code in {500, 502, 503, 504}:
                wait = backoff_factor ** attempt
                print(f"{response.status_code} Server Error. Retrying in {wait:.1f} seconds...")
                time.sleep(wait)
                attempt += 1
                continue
            
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
        else:
            raise Exception(f"❌ Authentication failed: {response.status_code}, {response.text}")


