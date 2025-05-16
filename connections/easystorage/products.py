from utils.logger import get_outlet_logger


class EasyStorageProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client
        self.products_endpoint = 'https://easystorage.engine.pancernik.local/api/v1/products/easystorage/'
        self.outlet_logger = get_outlet_logger().get_logger()


    def get_pancernik_products(self):
        
        try:
            params = {'account_id': self.client.pancernik_account_id}

            print('ℹ️  Downloading Pancernik products from EasyStorage...')
            self.outlet_logger.info('ℹ️ Downloading Pancernik products from EasyStorage...')
            
            response = self.client.session.request(method='GET', url=self.products_endpoint, params=params, verify=False)
            return response.json()
        
        except Exception as e:
            print(f"❌ Error downloading Pancernik products from EasyStorage: {e}")
            self.outlet_logger.critical(f"❌ Error downloading Pancernik products from EasyStorage: {e}")
            return None
    
    def get_bizon_products(self):

        try:
            params = {'account_id': self.client.bizon_account_id}

            print('ℹ️ Downloading Bizon products from EasyStorage...')
            self.outlet_logger.info('ℹ️ Downloading Bizon products from EasyStorage...')

            response = self.client.session.request(method='GET', url=self.products_endpoint, params=params, verify=False)
            return response.json()
        
        except Exception as e:
            print(f"❌ Error downloading Bizon products from EasyStorage: {e}")
            self.outlet_logger.critical(f"❌ Error downloading Bizon products from EasyStorage: {e}")

            return None
