import config
import pandas as pd

class ShoperAttributes:

    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    def get_all_attribute_groups(self):
        """Get all attribute groups from Shoper. Returns a pandas DataFrame if successful, None if failed"""
        attribute_groups = []
        page = 1
        url = f'{self.client.site_url}/webapi/rest/attribute-groups'

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
        df.to_excel(config.SHEETS_DIR / 'shoper_all_attribute_groups.xlsx', index=False)
        return df
    
    def get_all_attributes(self):
        """Get all attributes from Shoper. Returns a pandas DataFrame if successful, None if failed"""
        attributes = []
        page = 1
        url = f'{self.client.site_url}/webapi/rest/attributes'

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
        df.to_excel(config.SHEETS_DIR / 'shoper_all_attributes.xlsx', index=False)
        return df
    
    def get_attribute_group_by_id(self, attribute_group_id):
        """Get an attribute group by its ID
        Args:
            attribute_group_id (int): The ID of the attribute group to get
        Returns:
            dict: The attribute group data
        """
        url = f'{self.client.site_url}/webapi/rest/attribute-groups/{attribute_group_id}'
        
        response = self.client._handle_request('GET', url)
        
        if response.status_code != 200:
            print(f'❌ API Error: {response.status_code}, {response.text}')
            return None
        
        return response.json()

    def update_attribute_group_categories(self, attribute_group_id, categories):
        """Create an attribute group
        Args:
            attribute_group_id (int): The ID of the attribute group to create
            categories (list): Product categories list as integers
        """
        url = f'{self.client.site_url}/webapi/rest/attribute-groups/{attribute_group_id}'

        response = self.client._handle_request('PUT', url, json={'categories': categories})
        
        if response.status_code != 200:
            print(f'❌ API Error: {response.status_code}, {response.text}')
            return None
        
        return response.json()
