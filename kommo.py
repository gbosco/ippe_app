import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def get_kommo_headers():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    return headers
