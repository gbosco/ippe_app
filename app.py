import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Logar os headers da requisição
    print("Headers da Requisição:", request.headers)

    # Logar o corpo da requisição
    print("Corpo da Requisição:", request.data)

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

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run()
