import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

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
            
            author = data.get('message[add][0][author][id]', 'Autor Desconhecido')
            
            # Faça o processamento que você precisa com esses dados
            print(f"Texto da mensagem: {text}")
            print(f"Autor: {author}")

        except Exception as e:
            print("Erro ao processar a mensagem:", e)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run()
