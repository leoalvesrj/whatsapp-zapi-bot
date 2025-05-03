from flask import Flask, request, jsonify
from sheets import get_estoque, get_compras
from zapi import enviar_mensagem
from tagplus import consultar_financeiro

app = Flask(__name__)

@app.route("/webhook/zapi", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Requisição recebida:")
    print(data)

    try:
        # Verifica se a mensagem está no formato esperado
        if not data or 'text' not in data or 'message' not in data['text'] or 'phone' not in data:
            return jsonify({"error": "Formato de mensagem inválido"}), 400

        msg = data['text']['message'].strip()
        chat_id = data['phone']

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
        import traceback
        print("🟥 ERRO DETECTADO 🟥")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "bot ativo"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
