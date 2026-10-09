# MacTech v5: como atualizar

Este zip tem o projeto completo. Não precisas de enviar tudo para o GitHub:

- **Se já aplicaste a v4:** substitui só `app.py` e `assets.py`.
- **Se ainda não aplicaste a v4:** substitui estes 7: `app.py`, `assets.py`, `models.py`, `requirements.txt`, `ia.py`, `config.py`, `whatsapp.py`.

Os outros ficheiros não mudaram. Confirma que os nomes ficaram exatamente assim, sem `-1` nem `(1)`.

## Depois do deploy
1. `o-teu-site/saude` deve mostrar `"status":"ok"` e `"versao":"2026-10-08-g-v5"`. Outra versão = o Render ainda corre a antiga.
2. No painel, "Testar sistema" deve dizer que a IA respondeu.
3. Toca em **Descarregar cópia de segurança**: deve sair um ficheiro `.json`. Abre-o e confirma que tem as tuas empresas. Guarda-o em local privado (tem contactos de clientes).

## Se algo falhar
- **Build failed no Render:** copia a mensagem do log e manda-me.
- **Painel não abre ou botões sem resposta:** volta ao `assets.py` anterior (histórico do ficheiro no GitHub).
- **Voltar atrás em qualquer ficheiro:** GitHub, abre o ficheiro, *History*, restaura a versão anterior.

## Nota
Foi testado com simulações, não com a base de dados, a Meta ou o Gemini reais. O primeiro teste a sério são os 3 passos acima e uma mensagem de voz e uma foto no WhatsApp.
