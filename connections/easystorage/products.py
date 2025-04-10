

class EasyStorageProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.products_endpoint = 'https://easystorage.engine.pancernik.local/api/v1/products/easystorage/'

    def get_pancernik_products(self):
        
        try:
            params = {'account_id': self.client.pancernik_account_id}

            print('Downloading Pancernik products from EasyStorage...')
            response = self.client.session.request(method='GET', url=self.products_endpoint, params=params, verify=False)
            
            if response.status_code == 200:
                print('Products downloaded successfully.')

            return response.json()
        
        except Exception as e:
            print(f"Error downloading Pancernik products from EasyStorage: {e}")
            return None
    
    def get_bizon_products(self):

        try:
            params = {'account_id': self.client.bizon_account_id}

            print('Downloading Bizon products from EasyStorage...')
            response = self.client.session.request(method='GET', url=self.products_endpoint, params=params, verify=False)

            if response.status_code == 200:
                print('Products downloaded successfully.')

            return response.json()
        
        except Exception as e:
            print(f"Error downloading Bizon products from EasyStorage: {e}")
            return None
