import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print('X-Kommo-Secret:::', request.headers.get('X-Kommo-Secret'))

    # Logar os headers da requisição
    print("Headers da Requisição:", request.headers)

    # Logar o corpo da requisição
    print("Corpo da Requisição:", request.data)

    # Obter os dados do JSON enviado pelo Kommo CRM
    data = request.json
    
    # Logar os dados recebidos para ver no terminal ou logs do Heroku
    print("Dados recebidos:", data)

    return jsonify({'status': 'success'}), 200
