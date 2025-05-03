import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def resposta_gpt(mensagem_usuario):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um atendente inteligente da empresa, respondendo dúvidas gerais dos clientes de forma simpática e útil."},
            {"role": "user", "content": mensagem_usuario}
        ]
    )
    return resposta.choices[0].message['content'].strip()
