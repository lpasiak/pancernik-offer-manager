import config
import mimetypes
import json


class AllegroProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    # def upload_attachment(self, file):
    #     url = f'{config.ALLEGRO_API_URL}/sale/offer-attachments'
    #     file_path = file

    #     mime_type, _ = mimetypes.guess_type(file_path)
    #     mime_type = mime_type or 'application/pdf'

    #     metadata = {
    #         "type": "MANUAL",
    #         "file": {
    #             "name": file_path.name
    #         }
    #     }
    #     headers = {
    #         "Authorization": self.client.session.headers["Authorization"],
    #         "Accept": "application/vnd.allegro.public.v1+json"
    #     }

    #     with open(file_path, 'rb') as f:
    #         files = {
    #             'file': (file_path.name, f, mime_type),
    #             'metadata': (None, json.dumps(metadata), 'application/json')
    #         }

    #         response = self.client.session.request('POST', url, headers=headers, files=files)
    #         return response.json()
    