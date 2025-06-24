import config
import requests
from tqdm import tqdm


class EbayInventory:
    """In Ebay's InventoryAPI there are 3 items that make an offer published:
    inventory_item - an item in our warehouse
    offer - eBay listing draft
    listing_item - published eBay listing
    """
    def __init__(self, client):
        self.client = client

    """ Here is the section that manages inventory_items"""

    def get_all_inventory_items(self, limit=100, offset=100):
        try:
            url = 'https://api.ebay.com/sell/inventory/v1/inventory_item'
            
            all_offers = []
            offer_offset = 0
            offer_limit = 100
            params = {'limit': offer_limit, 'offset': offer_offset}

            response = self.client.session.request('GET', url, params=params)
            data = response.json()
            total_offers = data['total']

            for offset in tqdm(range(0, total_offers, offer_limit), desc='Downloading offers', unit= ' offer'):
                params['offset'] = offset
                response = self.client.session.request('GET', url, params=params)
                data = response.json()
                offers = data.get('inventoryItems')

                if not offers:
                    break

                all_offers.extend(offers)

            return all_offers
        
        except Exception as e:
            print(f'Error in eBay get_all_offers: {e}')

    def is_sku_valid(self, sku: str) -> bool:
        """Check if an SKU is valid: alphanumeric only, max 50 charsacters"""
        return isinstance(sku, str) and sku.isalnum() and len(sku) <= 50

    def get_all_inventory_items_sku_as_list(self, inventory_items: list) -> list:
        """Takes an export of Inventory List and returns all valid skus"""
        valid_skus = []
        invalid_skus = []

        for item in inventory_items:
            sku = item.get('sku', '').strip()

            if self.is_sku_valid(sku):
                valid_skus.append(sku)
            else:
                invalid_skus.append(sku)

        if invalid_skus:
            print(f"⚠️ Found {len(invalid_skus)} invalid SKUs")
            print(invalid_skus)

        return valid_skus

    def remove_inventory_item(self, sku):
        try:
            url = f'https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}'
            response = self.client.session.request('DELETE', url)

            if response.status_code == 204:
                print(f'✅ Successfully deleted SKU: {sku}')
            else:
                print(f'❌ Failed to delete SKU: {sku} - {response.status_code} - {response.text}')
        
        except Exception as e:
            print(f'Error in eBay remove_inventory_item: {e}')

    """ Here is the section that manages offers"""

    def get_all_offers(self):
        try:
            url = 'https://api.ebay.com/sell/inventory/v1/offer'
            
            params = {
                'limit': '5',
                'offset': '0'
            }
            response = self.client.session.request('GET', url, params=params)

            print(response.url)
            data = response.json()
            return data
        
        except Exception as e:
            print(f'Error in eBay get_all_offers: {e}')

    def get_a_single_offer_by_sku(self, sku):
        try:
            url = f'https://api.ebay.com/sell/inventory/v1/offer/{sku}'

            response = self.client.session.request('GET', url)
            data = response.json()
            print(response.headers)
            
            return data
        except Exception as e:
            print(f'Error in eBay get_a_single_offer: {e}')