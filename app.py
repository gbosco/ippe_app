import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Obter os dados do JSON enviado pelo Kommo CRM
    data = request.json
    
    print('---BOSCO---')

    # Logar os dados recebidos para ver no terminal ou logs do Heroku
    print("Dados recebidos:", data)

    # Extrair informações específicas do JSON
    if 'message' in data:
        message = data['message']
        print("Mensagem recebida:", message)
        
        # Processar a mensagem conforme necessário
        # Por exemplo, extrair conteúdo da mensagem
        text = message.get('text', 'Sem texto')
        sender = message.get('sender', 'Desconhecido')

        print("Texto da mensagem:", text)
        print("Remetente da mensagem:", sender)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run()
