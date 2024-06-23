import os
import requests
from config import  config as cfg

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def get_kommo_headers():
    return {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        'User-Agent': 'Kommo-oAuth-client/1.0'
    }


def get_leads(url: str):
    headers = get_kommo_headers()
    url = f"{url}/api/v4/leads?with=contact"
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        result = []
    else:
        result = response.json()['_embedded']['leads']

    return result


def get_contact_by_id(id):
    headers = get_kommo_headers()
    base_url = cfg.get("BASE_URL")
    url = f"{base_url}api/v4/contacts/{id}"
    response = requests.get(url, headers=headers)
    return response.json()