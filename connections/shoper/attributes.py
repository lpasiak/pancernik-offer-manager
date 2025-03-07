from ..shoper_connect import ShoperAPIClient
import config, os
import pandas as pd

class ShoperAttributes:

    def __init__(self, client=ShoperAPIClient):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_attribute_groups(self):
        
        attribute_groups = []
        page = 1
        url = f'{self.site_url}/webapi/rest/attribute-groups'

        print("Downloading all attribute groups.")
        while True:
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                print(f'❌ API Error: {response.status_code}, {response.text}')
                return None

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                break

            print(f'Page: {page}/{number_of_pages}')
            attribute_groups.extend(page_data)
            page += 1

        df = pd.DataFrame(attribute_groups)
        df.to_excel(os.path.join(self.sheets_dir, 'shoper_all_attribute_groups.xlsx'), index=False)
        return attribute_groups
    
    def get_all_attributes(self):
        attributes = []
        page = 1
        url = f'{self.site_url}/webapi/rest/attributes'

        print("Downloading all attributes.")
        while True:
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self.client._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                print(f'❌ API Error: {response.status_code}, {response.text}')
                return None

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                break

            print(f'Page: {page}/{number_of_pages}')
            attributes.extend(page_data)
            page += 1

        df = pd.DataFrame(attributes)
        df.to_excel(os.path.join(self.sheets_dir, 'shoper_all_attributes.xlsx'), index=False)
        return df