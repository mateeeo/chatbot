import os
from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Permite que o chat apareça em qualquer site de cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BANCO DE DADOS DE CLIENTES ---
# Aqui você gerencia quem pode usar seu serviço
CLIENTES = {
    os.getenv("LOJA1"): {
        "nome": "PetShop AuAu",
        "instrucoes": "Você é o atendente do PetShop AuAu. Foque em banho, tosa e rações premium."
    },
    os.getenv("LOJA2"): {
        "nome": "Advocacia Silva",
        "instrucoes": "Você é um assistente jurídico formal. Agende consultas e tire dúvidas básicas."
    },
    os.getenv("LOJA3"): {
        "nome": "Bot de Teste",
        "instrucoes": "Você é um assistente genérico e brincalhão."
    }
}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/chat")
async def chat(data: dict = Body(...)):
    token_cliente = data.get("token")
    user_message = data.get("message")

    # 1. Validação do Cliente
    if token_cliente not in CLIENTES:
        return {"reply": "Licença inválida ou pagamento pendente."}

    config = CLIENTES[token_cliente]

    # 2. Preparação da pergunta para a Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": config["instrucoes"]},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        res_json = response.json()
        
        if "choices" in res_json:
            return {"reply": res_json['choices'][0]['message']['content']}
        else:
            return {"reply": "Erro na API da Groq. Verifique saldo ou chave."}
            
    except Exception as e:
        return {"reply": f"Erro interno: {str(e)}"}
