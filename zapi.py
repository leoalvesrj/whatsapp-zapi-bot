import requests
import os

ZAPI_URL = os.getenv("ZAPI_URL")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")

def enviar_mensagem(chat_id, texto):
    url = f"{ZAPI_URL}/send-text"
    payload = {
        "chatId": chat_id,
        "text": texto
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(f"{url}?token={ZAPI_TOKEN}", json=payload, headers=headers)
    return response.status_code == 200
