import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENTES = {
    os.getenv("LOJA1"): {
        "nome": "PetShop AuAu",
        "instrucoes": "Você é o atendente do PetShop AuAu. Lembre-se do nome do cliente se ele disser."
    },
    os.getenv("LOJA2"): {
        "nome": "Advocacia Silva",
        "instrucoes": "Você é um assistente jurídico. Mantenha o histórico da conversa para entender o caso."
    }
}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/chat")
async def chat(data: dict = Body(...)):
    token_cliente = data.get("token")
    historico_recebido = data.get("historico", []) # Recebe a conversa inteira

    if token_cliente not in CLIENTES:
        return {"reply": "Licença inválida."}

    config = CLIENTES[token_cliente]

    # Montamos as mensagens para a Groq: System + Histórico
    mensagens_para_groq = [{"role": "system", "content": config["instrucoes"]}]
    
    # Adicionamos as últimas mensagens enviadas pelo JS (limitamos as últimas 10 para não travar)
    mensagens_para_groq.extend(historico_recebido[-10:])

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": mensagens_para_groq
    }

    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        res_json = response.json()
        return {"reply": res_json['choices'][0]['message']['content']}
    except Exception as e:
        return {"reply": "Erro ao processar conversa com memória."}
