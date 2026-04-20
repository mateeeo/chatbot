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

# Adicione seus clientes aqui
CLIENTES = {
    os.getenv("LOJA1"): {
        "nome": "PetShop AuAu",
        "instrucoes": "Você é o atendente do PetShop AuAu. Seja breve."
    }
}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/chat")
async def chat(data: dict = Body(...)):
    token_cliente = data.get("token")
    historico = data.get("historico", [])

    if token_cliente not in CLIENTES:
        return {"reply": "Erro: Token inválido."}

    if not GROQ_API_KEY:
        return {"reply": "Erro: Chave API não configurada na Vercel."}

    config = CLIENTES[token_cliente]
    
    mensagens = [{"role": "system", "content": config["instrucoes"]}]
    mensagens.extend(historico[-10:]) # Pega as últimas 10 mensagens

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": mensagens
    }

    try:
        response = requests.post(GROQ_URL, json=payload, headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        })
        res_json = response.json()
        
        # O pulo do gato: Verificar se a Groq respondeu corretamente
        if "choices" in res_json:
            return {"reply": res_json['choices'][0]['message']['content']}
        else:
            msg_erro = res_json.get("error", {}).get("message", "Erro desconhecido na Groq")
            return {"reply": f"Erro na Groq: {msg_erro}"}
            
    except Exception as e:
        return {"reply": f"Erro no servidor: {str(e)}"}
