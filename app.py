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
            messages = []
            for key, value in data.items():
                if key.startswith('message[add]'):
                    # Extrair partes da mensagem
                    parts = key.split('[')
                    if len(parts) > 3:
                        index = int(parts[2].strip(']'))
                        field = parts[3].strip(']')
                        if len(messages) <= index:
                            messages.append({})
                        messages[index][field] = value

            for message in messages:
                print("Processando mensagem:", message)
                text = message.get('text', 'Sem texto')
                author = message.get('author', {}).get('name', 'Desconhecido')
                chat_id = message.get('chat_id', 'Desconhecido')

                # Faça o processamento que você precisa com esses dados
                print(f"Texto da mensagem: {text}")
                print(f"Autor: {author}")
                print(f"ID do chat: {chat_id}")

        except Exception as e:
            print("Erro ao processar a mensagem:", e)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run()
