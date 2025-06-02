import config
import mimetypes
import json
from pathlib import Path
import requests


class AllegroProducts:
    def __init__(self, client):
        """Initialize a Shoper Client"""
        self.client = client

    # def upload_attachment(self):
    #     url = f'{config.ALLEGRO_API_URL}/sale/offer-attachments'
    #     file_path = Path(config.ROOT_DIR) / 'Instrukcje' / 'test.pdf'

    #     mime_type, _ = mimetypes.guess_type(file_path)
    #     mime_type = mime_type or 'application/pdf'

    #     # Do NOT include Content-Type manually
    #     headers = {
    #         "Authorization": self.client.session.headers["Authorization"],
    #         "Accept": config.ALLEGRO_API_VERSION,
    #         "Content-Type": config.ALLEGRO_API_VERSION
    #     }

    #     # Metadata must be passed as a form field (not JSON in the body!)
    #     metadata = {
    #         "type": "MANUAL",
    #         "file": {
    #             "name": file_path.name
    #         }
    #     }
    #     print('Sending headers: ', headers)
    #     print('Sending metadata: ', metadata)
    #     self.client.session.headers.pop("Content-Type", None)

    #     with open(file_path, "rb") as f:
    #         files = {
    #             "file": (file_path.name, f, mime_type),
    #             "metadata": (None, json.dumps(metadata), "application/json")
    #         }

    #         response = self.client.session.request('POST',
    #                                                url,
    #                                                headers=headers,
    #                                                files=files)

    #     try:
    #         response.raise_for_status()
    #         return response.json()
        
    #     except requests.exceptions.HTTPError:
    #         print("❌ Upload failed:", response.status_code, response.text)
    #         return response.json()
    
    def upload_attachment(self, file_path: Path, attachment_type="MANUAL"):
        url = f"{config.ALLEGRO_API_URL}/sale/offer-attachments"
        metadata = {
            "type": attachment_type,
            "file": {
                "name": file_path.name
            }}
        headers = {
            "Content-Type": "application/vnd.allegro.public.v1+json",
            "Accept": config.ALLEGRO_API_VERSION,
            'Authorization': self.client.session.headers['Authorization']
        }

        response = self.client.session.post(url, headers=headers, json=metadata)

        if response.status_code != 201:
            print("❌ Creating an Attachment Object unsuccesful", response.status_code, response.text)
            return response.json()
        
        attachment_id = response.json()["id"]
        upload_url = response.headers.get("Location")

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        print('Mime type: ', mime_type)

        with open(file_path, "rb") as f:
            headers = {
                "Accept": config.ALLEGRO_API_VERSION,
                "Content-Type": mime_type,
                'Authorization': self.client.session.headers['Authorization']
            }

            response = requests.put(upload_url, headers=headers, data=f)

            if response.status_code != 200:
                print("❌ Uploading an Attachment Object unsuccesful", response.status_code, response.text)
                return response.json()

            print("✅ Attachment added succesfully.")
            print(response.json())
            return response.json()