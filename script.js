(function() {
    // 1. CONFIGURAÇÕES - Mude aqui para cada cliente
    const CONFIG = {
        scriptUrl: "https://script.google.com/macros/s/AKfycbyc-acAjaQIevpX5cJkoYaN7PoiG0WAFismmYgyspaljG5EeUP5XztLaiITYmoXOZVX/exec",
        token: "chave-secreta-do-meu-cliente-001",
        nomeBot: "Assistente IA",
        corPrincipal: "#000000"
    };

    // 2. CRIAÇÃO DO HTML (Injetado dinamicamente)
    const chatHTML = `
        <div id="grok-container" style="position:fixed; bottom:20px; right:20px; z-index:999999; font-family: sans-serif;">
            <div id="grok-bubble" style="width:60px; height:60px; background:${CONFIG.corPrincipal}; border-radius:50%; cursor:pointer; display:flex; align-items:center; justify-content:center; color:white; font-size:24px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">💬</div>
            
            <div id="grok-window" style="display:none; position:absolute; bottom:80px; right:0; width:350px; height:500px; background:white; border-radius:12px; box-shadow:0 8px 24px rgba(0,0,0,0.2); flex-direction:column; overflow:hidden; border: 1px solid #eee;">
                <div style="background:${CONFIG.corPrincipal}; color:white; padding:15px; font-weight:bold; display:flex; justify-content:space-between;">
                    <span>${CONFIG.nomeBot}</span>
                    <span id="grok-close" style="cursor:pointer;">✕</span>
                </div>
                <div id="grok-messages" style="flex:1; padding:15px; overflow-y:auto; background:#f9f9f9; display:flex; flex-direction:column; gap:10px;"></div>
                
                <input type="text" id="grok-hp" style="display:none !important" tabindex="-1" autocomplete="off">
                
                <div style="padding:10px; background:white; border-top:1px solid #eee; display:flex;">
                    <input type="text" id="grok-input" placeholder="Digite sua mensagem..." style="flex:1; border:none; outline:none; padding:8px; font-size:14px;">
                    <button id="grok-send" style="background:none; border:none; cursor:pointer; font-weight:bold; color:${CONFIG.corPrincipal};">Enviar</button>
                </div>
            </div>
        </div>
    `;

    const div = document.createElement('div');
    div.innerHTML = chatHTML;
    document.body.appendChild(div);

    // 3. ELEMENTOS E LÓGICA
    const bubble = document.getElementById('grok-bubble');
    const window = document.getElementById('grok-window');
    const close = document.getElementById('grok-close');
    const input = document.getElementById('grok-input');
    const sendBtn = document.getElementById('grok-send');
    const msgBox = document.getElementById('grok-messages');
    let isWaiting = false;

    bubble.onclick = () => window.style.display = 'flex';
    close.onclick = () => window.style.display = 'none';

    function addMessage(sender, text) {
        const m = document.createElement('div');
        const isUser = sender === 'Você';
        m.style.cssText = `padding:8px 12px; border-radius:8px; max-width:80%; font-size:14px; line-height:1.4; ${isUser ? 'align-self:flex-end; background:#e3efff;' : 'align-self:flex-start; background:white; border:1px solid #ddd;'}`;
        m.innerHTML = `<strong>${sender}:</strong><br>${text}`;
        msgBox.appendChild(m);
        msgBox.scrollTop = msgBox.scrollHeight;
    }

    async function handleSend() {
        const text = input.value.trim();
        const hp = document.getElementById('grok-hp').value;

        if (hp !== "" || isWaiting || !text) return; // Bloqueia bots e envios múltiplos

        isWaiting = true;
        addMessage('Você', text);
        input.value = '...';
        input.disabled = true;

        try {
            const res = await fetch(CONFIG.scriptUrl, {
                method: 'POST',
                body: JSON.stringify({ message: text, token: CONFIG.token })
            });
            const data = await res.json();
            addMessage('IA', data.reply);
        } catch (e) {
            addMessage('Erro', 'Tente novamente em instantes.');
        } finally {
            isWaiting = false;
            input.value = '';
            input.disabled = false;
            input.focus();
        }
    }

    sendBtn.onclick = handleSend;
    input.onkeypress = (e) => { if(e.key === 'Enter') handleSend(); };

})();
