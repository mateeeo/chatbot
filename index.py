import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Configuração de CORS: Permite que o chat funcione em qualquer site
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pega a chave das "Environment Variables" da Vercel
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/chat")
async def chat(data: dict = Body(...)):
    user_message = data.get("message")
    token = data.get("token")

    # Validação de segurança simples
    if token != "chave-secreta-do-meu-cliente-001":
        return {"reply": "Acesso não autorizado."}

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [
            {"role": "system", "content": "Você é um assistente comercial prestativo."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        response_data = response.json()
        return {"reply": response_data['choices'][0]['message']['content']}
    except Exception as e:
        return {"reply": "Erro ao processar sua mensagem."}
