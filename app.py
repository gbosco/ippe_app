import os, requests
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)

#Que concede acesso do aplocativo
#https://www.kommo.com/oauth/?client_id=e921a2d5-d899-4252-9ae4-4fa11740eceb&state=1&mode=post_message
CLIENT_ID = os.getenv('KOMMO_SECRET_KEY')
CLIENT_SECRET = os.getenv('KOMMO_INTEGRATION_ID')
REDIRECT_URI = 'https://crm-ippe-6ccc57521801.herokuapp.com/'  # Use a URL apropriada para produção

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
            print("Processando mensagem:" )
            text = data.get('message[add][0][text]', 'Sem Texto')
            
            author = data.get('message[add][0][author][name]', 'Autor Desconhecido')
            
            # Faça o processamento que você precisa com esses dados
            print(f"Texto da mensagem: {text}")
            print(f"Autor: {author}")

        except Exception as e:
            print("Erro ao processar a mensagem:", e)

    return jsonify({'status': 'success'}), 200


@app.route('/')
def home():
    # URL para redirecionar o usuário para autorização
    #auth_url = f"https://marceloluizpereira.kommo.com/oauth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&state=YOUR_STATE"
    #https://kommo.com/oauth/?client_id=e921a2d5-d899-4252-9ae4-4fa11740eceb&state=1&mode=post_message&redirect_uri=https://crm-ippe-6ccc57521801.herokuapp.com/auth
    auth_url = f"https://www.kommo.com/oauth/?client_id={CLIENT_ID}&state=1&mode=post_message&redirect_uri={REDIRECT_URI}&response_type=code"
    print('auth_url *---> ', auth_url)
    #return redirect(auth_url)
    return CLIENT_ID + '###' + CLIENT_SECRET
    

@app.route('/auth')
def auth():
    code = request.args.get('code')
    if not code:
        return "Authorization code not found", 400

    # Trocar o código de autorização por um token de acesso
    token_url = 'https://marceloluizpereira.kommo.com/oauth2/access_token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, json=payload)
    token_data = response.json()

    # Salvar o token de acesso (você pode salvar no banco de dados ou variável de ambiente)
    access_token = token_data.get('access_token')
    os.environ['KOMMO_ACCESS_TOKEN'] = access_token
    
    print('KOMMO_ACCESS_TOKEN:', access_token)

    return "Authorization successful. Access token obtained."




if __name__ == '__main__':
    app.run()
