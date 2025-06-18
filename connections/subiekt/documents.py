import config
import json


class SubiektDocuments:
    def __init__(self, client):
        """Initialize a Subiekt Documents"""
        self.client = client

    def get_documents(self, database):
        documents_endpoint = f'{config.SUBIEKT_URL}/api/v1/{database['name']}/documents/lines?document_type=FZ&date_lte=2025-06-10&date_gte=2025-06-10'

        response = self.client.session.request('GET', url=documents_endpoint, verify=False)
        data = response.json()

        with open('subiekt_dokumenty.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return response.json()