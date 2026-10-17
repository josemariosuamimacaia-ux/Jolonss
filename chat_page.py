"""Página do chat web (link partilhável ou iframe): /c/<slug>."""

PAGINA = """<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{{ nome }} — atendimento</title>
<meta name="theme-color" content="#0b1b33"><link rel="icon" href="{% if cfg.logo %}/logo/{{ cfg.slug }}?v={{ cfg.logo }}{% else %}/static/logo.svg{% endif %}"><link rel="stylesheet" href="/static/chat.css"></head><body>
<header>{% if cfg.logo %}<img class="logo emp" src="/logo/{{ cfg.slug }}?v={{ cfg.logo }}" alt="{{ nome }}" width="48" height="48">{% else %}<img class="logo" src="/static/logo.svg" alt="MacTech" width="48" height="48">{% endif %}<div><b>{{ nome }}</b><small>Assistente virtual · sempre disponível</small></div><span class="tag">IA</span></header>
<div class="faixa"><span>Informação da própria empresa</span><span>Respostas imediatas</span><span>Assistente de IA identificado</span></div>
<main id="log" role="log" aria-live="polite"></main>
<form id="f"><input id="t" maxlength="1000" placeholder="Escreve a tua mensagem" autocomplete="off" aria-label="Mensagem"><button type="submit">Enviar</button></form>
<footer><img class="logo-mini" src="/static/logo.svg" alt="" width="16" height="16">Atendimento automático com IA · as conversas são guardadas para melhorar o serviço · MacTech</footer>
<script type="application/json" id="cfg">{{ cfg|tojson }}</script>
<script src="/static/chat.js"></script></body></html>"""
