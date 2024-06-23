import os
import requests
from flask import Flask, request, redirect, jsonify
from dotenv import load_dotenv, find_dotenv
from config import config as cfg
import chatgpt
import kommo

app = Flask(__name__)

base_url = "https://marceloluizpereira.kommo.com"

load_dotenv(find_dotenv())

#Que concede acesso do aplocativo
CLIENT_ID = os.getenv('KOMMO_INTEGRATION_ID')
CLIENT_SECRET = os.getenv('KOMMO_SECRET_KEY')
REDIRECT_URI = os.getenv('REDIRECT_URI')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.route('/send_msg')
def send_message():
    #chat_id = request.args.get('chat_id')
    chat_id = '8600bc3a-59d7-4f5f-a144-bfecbfe4e9a9'
    text = 'teste.....'
    url = 'https://marceloluizpereira.amocrm.com/api/v4/messages'

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@app.route('/webhook', methods=['POST'])
def webhook():
    # Tentar carregar o JSON manualmente
    try:
        if request.content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
            print("Dados recebidos (form):", data)
        else:
            data = request.get_json(force=True)
            print("Dados recebidos (json):", data)
    except Exception as e:
        data = None
        print("Erro ao decodificar JSON:", e)

    if data:
        # Processar a mensagem recebida
        try:
            print("Processando mensagem:")
            contact_id = data.get("message[add][0][contact_id]")
            text = data.get('message[add][0][text]', 'Sem Texto')
            author = data.get('message[add][0][author][name]', 'Autor Desconhecido')

            # Faça o processamento que você precisa com esses dados
            print(f"Texto da mensagem: {text}")
            print(f"Autor: {author}")

            if contact_id is None:
                return

            contact = kommo.get_contact_by_id(contact_id)
            lead_id = contact["_embedded"]["leads"][0][id]

            text_english = chatgpt.translate_text(text, "english")
            api_response = chatgpt.generate_text_response(text_english)
            text_portuguese = chatgpt.translate_text(api_response)

            payload = {
                "custom_fields_values": [
                    {
                        "field_id": cfg["LEADS_FIELDS"].get("CHATGPT_RESPONSE"),
                        "values": [{"value": text_portuguese}]
                    }
                ]
            }

            url = f"{base_url}/api/v4/leads/{lead_id}"
            headers = kommo.get_kommo_headers()
            patch_response = requests.patch(url, json=payload, headers=headers)
            print(patch_response)
            print("Set chatgpt generated response")

        except Exception as e:
            print("Erro ao processar a mensagem:", e)

    return jsonify({'status': 'success'}), 200


@app.route("/leads", methods=["GET"])
def get_leads():
    try:
        response, status = kommo.get_leads(base_url)
        print(response)
    except Exception as e:
        print(e)
        return str(e), 500


# Webhook to listen when new lead added
@app.route('/webhook/lead', methods=['POST'])
def lead_webhook():
    try:
        if request.content_type == 'application/x-www-form-urlencoded':
            data = request.form.to_dict()
            print("Dados recebidos (form):", data)
        else:
            data = request.get_json(force=True)
            print("Dados recebidos (json):", data)
    except Exception as e:
        data = None
        print("Erro ao decodificar JSON:", e)

    if data:
        # Processar a mensagem recebida
        try:
            print("Processando mensagem:")

            new_leads = data.get("add")

            for lead in new_leads:
                print(lead)
                headers = kommo.get_kommo_headers()
                payload = {
                    "id": cfg["LEADS_FIELDS"].get("CHATGPT_RESPONSE"),
                    "name": "chatgpt_response",
                    "type": "text",
                    "is_api_only": True
                }
                response = requests.patch(f"{base_url}/api/v4/leads/custom_field", data=payload, headers=headers)
                status_code = response.status_code
                if status_code == 200:
                    print("custom field added successfully")
                else:
                    print("error adding custom field")

        except Exception as e:
            print("Erro ao processar a mensagem:", e)

    return jsonify({'status': 'success'}), 200


@app.route('/')
def home():
    # URL para redirecionar o usuário para autorização
    #auth_url = f"https://marceloluizpereira.kommo.com/oauth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&state=YOUR_STATE"
    #https://kommo.com/oauth/?client_id=e921a2d5-d899-4252-9ae4-4fa11740eceb&state=1&mode=post_message&redirect_uri=https://crm-ippe-6ccc57521801.herokuapp.com/auth
    auth_url = f"https://www.kommo.com/oauth/?client_id={CLIENT_ID}&state=xyz&mode=post_message&redirect_uri={REDIRECT_URI}&response_type=code"
    print('auth_url *---> ', auth_url)
    return redirect(auth_url)


@app.route('/auth')
def auth():
    code = request.args.get('code')
    if not code:
        return "Authorization code not found", 400

    # Trocar o código de autorização por um token de acesso
    token_url = f"{base_url}/oauth2/access_token"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, json=payload, headers=headers)
    token_data = response.json()

    # Salvar o token de acesso (você pode salvar no banco de dados ou variável de ambiente)
    access_token = token_data.get('access_token')
    #os.environ['KOMMO_ACCESS_TOKEN'] = access_token

    print('request.content_type:', request.content_type)
    print('json:', token_data)
    print('KOMMO_ACCESS_TOKEN:', access_token)

    return "Authorization successful. Access token obtained."


if __name__ == '__main__':
    app.run()
