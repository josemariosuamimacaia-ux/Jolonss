# Parte visual — como atualizar

Isto é só a parte **visual** do portal da empresa (botões e layout).

## O que muda visualmente
- Botão **Ver conversa** (contorno)
- Botão **Apagar dados** (vermelho suave)
- Melhor espaçamento e alinhamento das conversas

## Ficheiros

1. **minha_js_visual.js**  
   Substitui o conteúdo de `ASSETS["minha.js"]` no teu `assets.py`.

2. **painel_css_extra.css**  
   Cola o conteúdo no final do CSS de `"painel.css"` dentro de `ASSETS` no `assets.py`.

## Passos rápidos
1. Abre o teu `assets.py`.
2. Procura `ASSETS["minha.js"]` e substitui o JavaScript pelo conteúdo de `minha_js_visual.js`.
3. Procura o CSS de `"painel.css"` e cola no final o conteúdo de `painel_css_extra.css`.
4. Faz commit + deploy no Render.

Depois do deploy, entra em `/minha-empresa` e vais ver os botões novos nas conversas.

Nota: a parte interna (models, privacidade, auditoria) já está no ZIP anterior. Isto é só o visual.
