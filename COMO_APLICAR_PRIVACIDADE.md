# MacTech — Privacidade + Auditoria (funcionalidade original)

Feito para um único fundador. Não copia Respond.io nem ManyChat.
Dá às empresas angolanas algo que os bots baratos não têm: **consentimento registado + direito a ser esquecido + registo de quem mexeu nos dados**.

## O que foi adicionado

1. **Consentimento**  
   Na primeira mensagem do cliente a conversa fica marcada com `consentiu_em`.  
   Serve para provar que a pessoa continuou a falar depois de saber que a conversa é guardada.

2. **Apagar dados do cliente**  
   - No portal da empresa (`/minha-empresa`): botão em cada conversa.  
   - No painel do dono: também pode apagar.  
   Apaga mensagens e contacto. Mantém a linha da conversa só para estatísticas anónimas.

3. **Tabela de auditoria**  
   Regista ações importantes (apagar cliente, etc.) sem guardar o texto das mensagens.  
   O dono vê em `GET /api/auditoria`.

4. **Aviso forte se faltar ENCRYPTION_KEY**  
   Tokens do WhatsApp deixam de ficar “em silêncio” em texto simples.

## Ficheiros a substituir / acrescentar (raiz do GitHub)

| Ficheiro | Ação |
|----------|------|
| `models.py` | **Substituir** pelo que está nesta pasta |
| `segredos.py` | **Substituir** pelo que está nesta pasta |
| `privacidade.py` | **Acrescentar** (ficheiro novo) |
| `app.py` | **Pequenas alterações** (ver abaixo) |
| `assets.py` | **Pequenas alterações** no portal (ver abaixo) |

As colunas novas (`consentiu_em`, `retencao_dias`) e a tabela `auditoria` são criadas sozinhas no arranque (migração automática).

---

## Alterações em `app.py` (copia e cola)

### 1. No topo, junto dos outros imports

Procura a linha:
```python
from models import (URL_ERRO, URL_INVALIDA, Conversa, Departamento, Empresa, Encomenda, Mensagem, Produto, SessionLocal,
                    Ticket, agora, descrever_erro_db, init_db)
```

Troca por:
```python
from models import (URL_ERRO, URL_INVALIDA, Auditoria, Conversa, Departamento, Empresa, Encomenda, Mensagem, Produto, SessionLocal,
                    Ticket, agora, descrever_erro_db, init_db)
import privacidade
```

### 2. Depois de `nivel4.registar(...)` e `publico.registar(...)` (perto do fim do ficheiro)

Acrescenta:
```python
privacidade.registar(app, exige_admin, exige_empresa, iso_utc)
```

### 3. Dentro da função `guardar` (ou logo depois de criar a mensagem do utilizador no chat web e no WhatsApp)

Onde guardas a mensagem do cliente (`remetente == "user"`), chama:
```python
from privacidade import marcar_consentimento
marcar_consentimento(conversa)
```

No chat web (`chat_mensagem` e `chat_stream`), logo após:
```python
mu = guardar(db, conversa, "user", texto)
```
acrescenta:
```python
marcar_consentimento(conversa)
```

No WhatsApp (`_processar`), no mesmo sítio (depois de `guardar` a mensagem do user), o mesmo.

### 4. (Opcional mas recomendado) Registar no backup

Na lista `_BACKUP` (se existir), podes ignorar a tabela `auditoria` — não precisa de ir no backup de catálogo.

---

## Alterações em `assets.py` (portal da empresa)

No JavaScript de `minha.js` (dentro de `ASSETS["minha.js"]`), na parte que desenha as conversas, acrescenta um botão “Apagar dados”.

Procura o sítio onde faz:
```javascript
d.appendChild(h('p', 'msg', c.ultima || ''));
```

E troca o bloco das conversas por algo assim (mantém o resto igual):

```javascript
r.conversas.forEach(function (c) {
  var d = h('div', 'item'); d.style.cursor = 'pointer';
  d.appendChild(h('b', null, c.canal + (c.contacto ? ' · ' + c.contacto : '') + (c.humano ? ' · à espera de pessoa' : '')));
  d.appendChild(h('p', 'msg', c.ultima || ''));
  var row = h('div', 'row');
  var bVer = h('button', 'btn alt', 'Ver'); bVer.type = 'button';
  bVer.onclick = function (ev) {
    ev.stopPropagation();
    api('GET', '/api/minha/conversa/' + c.id).then(function (j) {
      var T = $('tr'); T.textContent = '';
      j.mensagens.forEach(function (m) {
        T.appendChild(h('p', 'msg', (m.remetente === 'user' ? 'Cliente: ' : m.remetente === 'human' ? 'Equipa: ' : 'IA: ') + m.conteudo));
      });
      T.scrollIntoView();
    }).catch(function (x) { alert(x.message); });
  };
  var bAp = h('button', 'btn alt', 'Apagar dados'); bAp.type = 'button';
  bAp.onclick = function (ev) {
    ev.stopPropagation();
    if (!confirm('Apagar todas as mensagens e o contacto deste cliente? Esta ação não pode ser desfeita.')) return;
    api('POST', '/api/minha/apagar-cliente', { conversa_id: c.id }).then(function () {
      carregar();
    }).catch(function (x) { alert(x.message); });
  };
  row.appendChild(bVer); row.appendChild(bAp); d.appendChild(row);
  C.appendChild(d);
});
```

(Se preferires, posso entregar o `minha.js` completo já com o botão.)

---

## Depois do deploy

1. Abre `/saude` — deve continuar `"status":"ok"`.
2. No Render → Environment, define `ENCRYPTION_KEY` (gera com o comando do `segredos.py`).
3. Entra no portal de uma empresa, abre uma conversa e testa **Apagar dados**.
4. Como dono: `GET /api/auditoria` com a tua chave de admin — deve aparecer a ação.

## O que NÃO foi feito (de propósito)

- Não meti Redis (custa ou complica o plano grátis).
- Não meti 2FA (podes pedir depois).
- Não apago conversas antigas automaticamente (só o botão manual). Assim não há surpresas.

Se quiseres o próximo passo (botão também no painel do dono + lista de auditoria no ecrã), diz e eu entrego o `assets.py` completo.
