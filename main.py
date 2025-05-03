from flask import Flask, request, jsonify
from sheets import get_estoque, get_compras
from zapi import enviar_mensagem
from tagplus import consultar_financeiro

app = Flask(__name__)

@app.route("/webhook/zapi", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📥 Requisição recebida:")
        print(data)

        # Validação segura para evitar erros de chave
        if not data or "text" not in data or "message" not in data["text"]:
            return jsonify({"error": "Formato de payload inválido."}), 400

        msg = data["text"]["message"].strip()
        chat_id = data.get("chatLid") or data.get("phone")

        if not chat_id:
            return jsonify({"error": "chatId não encontrado."}), 400

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
        else:
            print("Mensagem ignorada:", msg)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("Erro:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "bot ativo"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
