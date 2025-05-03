from flask import Flask, request, jsonify
from sheets import get_estoque, get_compras
from zapi import enviar_mensagem
from tagplus import consultar_financeiro

app = Flask(__name__)

@app.route("/webhook/zapi", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        msg = data['message']['text'].strip()
        chat_id = data['message']['chatId']

        if msg.startswith("!"):
            comando = msg.lower().replace("!", "").strip()
            if comando == "estoque":
                resposta = get_estoque()
            elif comando == "compras":
                resposta = get_compras()
            elif comando == "financeiro":
                resposta = consultar_financeiro()
            else:
                resposta = "Comando não reconhecido. Use !estoque, !compras ou !financeiro."

            enviar_mensagem(chat_id, resposta)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "bot ativo"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

