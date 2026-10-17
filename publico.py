"""Páginas públicas da MacTech: início com 3 botões, lista de empresas para clientes e registo de empresas.

Só o Dono (botão "Dono" -> /painel) usa a chave de administração. Clientes e empresas nunca a veem.
Empresas que se registam sozinhas ficam 'pendentes' (invisíveis aos clientes) até o dono confirmar o
pagamento e carregar em "Ativar (pagou)" no painel."""
import base64
import hashlib
import logging
import os
import re

from flask import Response, g, jsonify, render_template_string, request
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, Empresa, SessionLocal, agora, engine
from segredos import nova_chave_acesso

log = logging.getLogger("mactech.publico")


class PedidoEmpresa(Base):
    """Dados de contacto e de pagamento de uma empresa que se registou sozinha (só o dono os vê)."""
    __tablename__ = "pedidos_empresa"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    contacto: Mapped[str] = mapped_column(String(120))
    ref_pagamento: Mapped[str] = mapped_column(String(120))
    aceitou_termos_em: Mapped[object] = mapped_column(DateTime(timezone=True), default=agora)


class LogoEmpresa(Base):
    """Logótipo da empresa (imagem pequena guardada em base64). Aparece no chat e na lista de empresas."""
    __tablename__ = "logos_empresa"
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(20))
    dados: Mapped[str] = mapped_column(Text)
    versao: Mapped[str] = mapped_column(String(16))


Base.metadata.create_all(engine)   # cria só a tabela nova, se ainda não existir

TERMOS = """MODELO DE TERMOS (o dono deve rever e adaptar com um advogado antes de usar com clientes reais)

1. Serviço: a MacTech fornece um assistente de atendimento com inteligência artificial, que responde a clientes da empresa por chat e/ou WhatsApp com base nas informações que a empresa fornece.
2. Informação da empresa: a empresa é responsável pela exactidão e actualização das informações (produtos, preços, horários). O assistente usa apenas essas informações, mas pode cometer erros; a empresa deve acompanhar as conversas.
3. Pagamento: o serviço é activado depois de a MacTech confirmar o pagamento inicial. Sem pagamento confirmado, a empresa não aparece aos clientes.
4. Teste: as empresas abordadas pela MacTech podem ter um período de teste gratuito de 1 dia.
5. Dados: as conversas entre clientes e o assistente são guardadas para prestar o serviço e melhorar o atendimento. A empresa deve informar os seus clientes disso.
6. Suspensão: a MacTech pode suspender o serviço por falta de pagamento, uso abusivo ou conteúdo ilegal.
7. Limites: o serviço pode ficar indisponível por falhas técnicas ou dos fornecedores de IA, sem que isso dê direito a indemnização."""

# ---------- páginas ----------
ICONES = {
    "cliente": '<svg viewBox="0 0 24 24"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/></svg>',
    "empresa": '<svg viewBox="0 0 24 24"><path d="M4 21V5l8-2v18M12 9h8v12M7 9h2M7 13h2M7 17h2M15 13h2M15 17h2"/></svg>',
    "entrar": '<svg viewBox="0 0 24 24"><path d="M14 4h5v16h-5M10 8l4 4-4 4M14 12H4"/></svg>',
    "dono": '<svg viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.4 7.7-8 9-4.6-1.3-8-4.5-8-9V6l8-3z"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
}

BASE_CSS = """<style>
:root{--bg:#e4e9f2;--card:#fff;--ink:#0c1a2e;--mut:#55647f;--acc:#14396b;--accT:#fff;--gold:#d4ac52;--goldd:#9a7220;--line:#d5dce9;--nav:#0b1b33;--tint:rgba(154,114,32,.11);--sh:0 1px 2px rgba(11,27,51,.06),0 8px 24px rgba(11,27,51,.07)}
@media(prefers-color-scheme:dark){:root{--bg:#03070d;--card:#101e34;--ink:#e8eef8;--mut:#93a3bf;--acc:#e0b85c;--accT:#0b1b33;--gold:#e0b85c;--goldd:#e0b85c;--line:#1f3354;--nav:#060f20;--tint:rgba(224,184,92,.12);--sh:none}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 "Segoe UI",system-ui,-apple-system,Roboto,sans-serif;-webkit-font-smoothing:antialiased}
.topo{background:var(--nav);box-shadow:inset 0 -3px 0 var(--gold)}
.topo div{max-width:620px;margin:0 auto;padding:11px 18px;display:flex;align-items:center;gap:11px}
.topo a{display:flex;align-items:center;gap:11px;color:#fff;text-decoration:none;font-size:19px;font-weight:700;letter-spacing:-.01em}
.topo span{color:var(--gold)}.topo small{margin-left:auto;color:rgba(255,255,255,.7);font-size:12.5px}
.lg{width:40px;height:40px;border-radius:50%;box-shadow:0 0 0 2px rgba(212,172,82,.6);flex:none}
main{max-width:620px;margin:0 auto;padding:22px 18px 40px}
h1{font-size:30px;line-height:1.2;letter-spacing:-.02em;margin:6px 0 6px}h1 span{color:var(--goldd)}
p{color:var(--mut);margin:6px 0}
a{color:var(--acc)}
.voltar{display:inline-block;margin:0 0 10px;font-size:14px;font-weight:600;text-decoration:none}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;margin:12px 0;box-shadow:var(--sh)}
.card>b{font-size:17px}
.card details{margin-top:8px;color:var(--mut)}.card summary{cursor:pointer;color:var(--acc);font-weight:600}
.btn{display:block;width:100%;margin:10px 0;background:var(--acc);color:var(--accT);border:0;border-radius:12px;padding:14px 20px;font:700 16px "Segoe UI",system-ui,sans-serif;text-align:center;text-decoration:none;cursor:pointer}
.btn.alt{background:transparent;color:var(--acc);border:1.5px solid var(--acc)}
label{display:block;margin-top:12px;font-weight:600;font-size:14.5px}
input,textarea{width:100%;border:1px solid var(--line);border-radius:12px;padding:11px 12px;font:16px "Segoe UI",system-ui,sans-serif;background:var(--bg);color:var(--ink)}
input:focus,textarea:focus{border-color:var(--goldd);outline:0;box-shadow:0 0 0 3px var(--tint)}
.btn:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--goldd);outline-offset:2px}
.msg{min-height:1.4em}.erro{color:#b3261e}.ok{color:#127a43;font-weight:600}
pre{white-space:pre-wrap;font:14px/1.45 system-ui;margin:8px 0 0;color:var(--mut)}
.h{position:absolute;left:-9999px}
.marca{text-align:center;margin:6px 0 22px}.marca h1{font-size:38px;margin:14px 0 6px}.marca p{font-size:17px;max-width:42ch;margin:0 auto}
.marca .lg{width:116px;height:116px;box-shadow:0 0 0 3px var(--gold)}
.op{display:grid;grid-template-columns:44px 1fr 18px;gap:1px 14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:15px 16px;margin:10px 0;text-decoration:none;color:var(--ink);box-shadow:var(--sh);transition:border-color .15s,background-color .15s}
.op:hover{border-color:var(--goldd);background:var(--tint)}
.op .ic{grid-column:1;grid-row:1/span 2;width:44px;height:44px;border-radius:12px;background:var(--nav);color:var(--gold);display:grid;place-items:center}
.op b{grid-column:2;grid-row:1;align-self:end;font-size:17px;line-height:1.3}.op small{grid-column:2;grid-row:2;min-width:0;font-size:14px;color:var(--mut);line-height:1.4}
.op>svg{grid-column:3;grid-row:1/span 2;width:18px;height:18px;stroke:var(--mut)}
svg{fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.op .ic svg{width:22px;height:22px}
.vant{display:flex;flex-wrap:wrap;gap:6px 18px;justify-content:center;margin:22px 0 0;font-size:13.5px;color:var(--mut)}
.vant span::before{content:"\\2713";color:var(--goldd);font-weight:700;margin-right:6px}
.pesq{position:relative;margin:12px 0 4px}.pesq svg{position:absolute;left:13px;top:50%;width:19px;height:19px;margin-top:-9.5px;stroke:var(--mut)}.pesq input{padding-left:42px}
.emp{display:grid;grid-template-columns:52px 1fr;gap:2px 14px;align-items:center;text-decoration:none;color:var(--ink);transition:border-color .15s,background-color .15s}
.emp:hover{border-color:var(--goldd);background:var(--tint)}
.av{width:52px;height:52px;border-radius:14px;background:var(--nav);color:var(--gold);display:grid;place-items:center;font-weight:700;font-size:22px;overflow:hidden;grid-row:span 3;border:1px solid var(--line)}
.av img{width:100%;height:100%;object-fit:contain;background:#fff;display:block}
.emp b{font-size:17px;line-height:1.3}.emp small{color:var(--mut);font-size:14px;line-height:1.4}
.emp .tg{justify-self:start;font-size:12px;font-weight:700;color:var(--goldd);background:var(--tint);border-radius:999px;padding:1px 10px}
.emp .ir{font-size:13.5px;font-weight:700;color:var(--acc)}
.passo{display:grid;grid-template-columns:34px minmax(0,1fr);gap:0 12px}
.passo .n{grid-row:span 2;width:34px;height:34px;border-radius:50%;background:var(--nav);color:var(--gold);display:grid;place-items:center;font-weight:700}
.passo>b{font-size:17px;align-self:center}.passo>p{margin:0 0 4px;font-size:14px}.passo>details,.passo>pre{grid-column:2}.passo>div{grid-column:1/-1;min-width:0}
.lgf{display:flex;align-items:center;gap:14px;margin-top:6px}.lgf canvas{width:64px;height:64px;border-radius:14px;border:1px dashed var(--line);background:var(--bg);flex:none}
.lgf input{padding:8px}
.nota{font-size:13px;color:var(--mut);margin:4px 0 0}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style><link rel="icon" href="/static/logo.svg">"""

TOPO = """<header class="topo"><div><a href="/"><img class="lg" src="/static/logo.svg" alt="" width="40" height="40"><b>Mac<span>Tech</span></b></a><small>Atendimento com IA</small></div></header>"""

INICIO = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b1b33"><title>MacTech</title>""" + BASE_CSS + """</head><body>""" + TOPO + """<main>
<div class="marca"><img class="lg" src="/static/logo.svg" alt="MacTech" width="116" height="116"><h1>Mac<span>Tech</span></h1>
<p>Assistentes de atendimento com IA para empresas.</p></div>
<a class="op" href="/clientes"><span class="ic">""" + ICONES["cliente"] + """</span><b>Sou cliente</b><small>Escolha uma empresa e tire as suas dúvidas com o assistente, a qualquer hora.</small><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></a>
<a class="op" href="/empresas"><span class="ic">""" + ICONES["empresa"] + """</span><b>Sou uma empresa</b><small>Registe o seu negócio e tenha um assistente com o seu nome e o seu logótipo.</small><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></a>
<a class="op" href="/minha-empresa"><span class="ic">""" + ICONES["entrar"] + """</span><b>Já sou empresa</b><small>Entre com a sua chave para atualizar informações, mudar o logótipo e ver conversas.</small><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></a>
<a class="op" href="/painel"><span class="ic">""" + ICONES["dono"] + """</span><b>Dono</b><small>Área reservada à administração da MacTech.</small><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></a>
<div class="vant"><span>Respostas imediatas</span><span>Passa a uma pessoa quando precisa</span><span>Chat e WhatsApp</span></div>
</main></body></html>"""

CLIENTES = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b1b33"><title>MacTech · Empresas</title>""" + BASE_CSS + """</head><body>""" + TOPO + """<main>
<a class="voltar" href="/">&larr; Início</a>
<h1>Escolha a empresa</h1>
<p>Toque na empresa com quem quer falar. O assistente responde de imediato e, se precisar, passa a conversa a uma pessoa.</p>
<div class="pesq">""" + ICONES["lupa"] + """<input id="q" placeholder="Procurar empresa" aria-label="Procurar empresa"></div>
<div id="lista"></div><p id="vazio" class="msg"></p>
<script>
var todas = [];
function mostrar() {
  var q = document.getElementById('q').value.toLowerCase(), L = document.getElementById('lista');
  L.textContent = '';
  var f = todas.filter(function (e) { return e.nome.toLowerCase().indexOf(q) >= 0; });
  f.forEach(function (e) {
    var a = document.createElement('a'); a.className = 'card emp'; a.href = '/c/' + encodeURIComponent(e.slug);
    var av = document.createElement('div'); av.className = 'av';
    if (e.logo) { var im = document.createElement('img'); im.src = '/logo/' + encodeURIComponent(e.slug) + '?v=' + encodeURIComponent(e.logo); im.alt = ''; av.appendChild(im); }
    else av.textContent = (e.nome || '?').slice(0, 1).toUpperCase();
    a.appendChild(av);
    var b = document.createElement('b'); b.textContent = e.nome; a.appendChild(b);
    var d = document.createElement('small'); d.textContent = e.resumo || 'Atendimento com assistente virtual.'; a.appendChild(d);
    var l = document.createElement('span');
    if (e.sector) { l.className = 'tg'; l.textContent = e.sector; } else { l.className = 'ir'; l.textContent = 'Conversar agora'; }
    a.appendChild(l); L.appendChild(a);
  });
  document.getElementById('vazio').textContent = f.length ? '' : (todas.length ? 'Nenhuma empresa encontrada.' : 'Ainda não há empresas disponíveis.');
}
fetch('/api/publico/empresas').then(function (r) { return r.json(); }).then(function (j) { todas = j.empresas || []; mostrar(); })
  .catch(function () { document.getElementById('vazio').textContent = 'Não foi possível carregar a lista. Tente de novo.'; });
document.getElementById('q').oninput = mostrar;
</script></main></body></html>"""

EMPRESAS = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b1b33"><title>MacTech · Registar empresa</title>""" + BASE_CSS + """</head><body>""" + TOPO + """<main>
<a class="voltar" href="/">&larr; Início</a>
<h1>Registar empresa</h1>
<p>Em três passos o seu negócio fica com um assistente de atendimento com IA, com o seu nome e o seu logótipo.</p>
<div class="card passo"><span class="n">1</span><b>Termos</b><p>Leia as condições do serviço antes de continuar.</p><details><summary>Ler os termos</summary><pre>{{ termos }}</pre></details></div>
<div class="card passo"><span class="n">2</span><b>Pagamento inicial</b><p>Faça o pagamento e guarde a referência para o passo seguinte.</p><pre>{{ pagamento }}</pre></div>
<form id="f" class="card passo"><span class="n">3</span><b>Dados da empresa</b><p>O assistente só usa estas informações para responder aos seus clientes.</p><div>
<label for="n">Nome da empresa</label><input id="n" maxlength="120" required>
<label for="lg">Logótipo (opcional)</label>
<div class="lgf"><canvas id="lgp" width="64" height="64" aria-label="Pré-visualização do logótipo"></canvas><input id="lg" type="file" accept="image/png,image/jpeg,image/webp"></div>
<p class="nota">PNG, JPG ou WebP. Aparece no chat dos seus clientes e na lista de empresas. Pode mudá-lo depois em Minha empresa.</p>
<label for="s">Sector (ex.: loja de tecnologia, clínica)</label><input id="s" maxlength="120">
<label for="d">O que a empresa faz</label><textarea id="d" rows="2" maxlength="1000"></textarea>
<label for="p">Produtos ou serviços (um por linha, com preços e detalhes)</label><textarea id="p" rows="5" maxlength="8000" required></textarea>
<label for="h">Horário</label><input id="h" maxlength="200">
<label for="l">Contactos e localização</label><input id="l" maxlength="300">
<label for="g">Garantia, entrega e pagamento</label><textarea id="g" rows="2" maxlength="1000"></textarea>
<label for="c">O seu telefone ou email (só a MacTech vê)</label><input id="c" maxlength="120" required>
<label for="r">Referência ou comprovativo do pagamento (número da transferência)</label><input id="r" maxlength="120" required>
<input class="h" id="w" tabindex="-1" autocomplete="off" aria-hidden="true">
<label style="display:flex;gap:8px;align-items:center"><input type="checkbox" id="t" style="width:auto"> Li e aceito os termos</label>
<button class="btn" type="submit">Enviar pedido</button>
<p id="m" class="msg"></p></div></form>
<script src="/static/logo.js"></script>
<script>
var logo = null;
function v(i) { return document.getElementById(i).value.trim(); }
document.getElementById('lg').onchange = function () {
  var m = document.getElementById('m'); m.className = 'msg'; m.textContent = '';
  MTLogo.ler(this.files[0]).then(function (r) {
    logo = r.url; var c = document.getElementById('lgp'); MTLogo.desenhar(c, r.canvas);
  }).catch(function (x) { logo = null; m.className = 'msg erro'; m.textContent = x.message; });
};
document.getElementById('f').onsubmit = function (ev) {
  ev.preventDefault();
  var m = document.getElementById('m'); m.className = 'msg'; m.textContent = 'A enviar...';
  fetch('/api/publico/registar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
    nome: v('n'), sector: v('s'), descricao: v('d'), produtos: v('p'), horario: v('h'), local: v('l'), politicas: v('g'),
    contacto: v('c'), ref_pagamento: v('r'), aceita_termos: document.getElementById('t').checked, website: v('w'), logo: logo }) })
    .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
    .then(function (x) {
      if (x.ok) { m.className = 'msg ok'; m.textContent = 'Pedido enviado. GUARDE esta chave (não volta a ser mostrada): ' + (x.j.chave || '') + ' . Serve para entrar em Minha empresa e ver o estado. Quando o pagamento for confirmado, a empresa fica disponível aos clientes.'; document.getElementById('f').reset(); logo = null; MTLogo.desenhar(document.getElementById('lgp'), null); }
      else { m.className = 'msg erro'; m.textContent = x.j.erro || 'Não foi possível enviar.'; }
    }).catch(function () { m.className = 'msg erro'; m.textContent = 'Sem ligação. Tente de novo.'; });
};
</script></main></body></html>"""


def _prompt(d, f):
    """Mesmo formato do formulário do painel."""
    linhas = [l.strip() for l in f["produtos"].split("\n") if l.strip()]
    return (f["nome"] + (f" ({f['sector']})" if f["sector"] else "") + ". " + f["descricao"] + "\nProdutos e serviços:\n"
            + "\n".join("- " + l for l in linhas)
            + (f"\nHorário: {f['horario']}" if f["horario"] else "")
            + (f"\nContactos e localização: {f['local']}" if f["local"] else "")
            + (f"\nGarantia, entrega e pagamento: {f['politicas']}" if f["politicas"] else ""))


_PNG, _JPG = b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff"


def _ler_logo(valor):
    """Valida um logótipo enviado como 'data:image/...;base64,...'. Devolve (tipo, base64, versao) ou None.
    Só PNG, JPEG e WebP (nunca SVG, que pode levar scripts). Máximo ~300 KB."""
    m = re.fullmatch(r"data:image/(?:png|jpeg|webp);base64,([A-Za-z0-9+/=]+)", str(valor or ""))
    if not m or len(m.group(1)) > 440_000:
        return None
    try:
        raw = base64.b64decode(m.group(1), validate=True)
    except Exception:
        return None
    if len(raw) > 320_000:
        return None
    if raw.startswith(_PNG):
        tipo = "image/png"
    elif raw.startswith(_JPG):
        tipo = "image/jpeg"
    elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        tipo = "image/webp"
    else:
        return None
    return tipo, m.group(1), hashlib.sha1(raw).hexdigest()[:10]


def _guardar_logo(db, empresa_id, logo):
    linha = db.get(LogoEmpresa, empresa_id)
    if linha:
        linha.tipo, linha.dados, linha.versao = logo
    else:
        db.add(LogoEmpresa(empresa_id=empresa_id, tipo=logo[0], dados=logo[1], versao=logo[2]))


def logo_versao(empresa_id):
    """'' se a empresa não tem logótipo; senão um código curto (muda quando o logótipo muda)."""
    with SessionLocal() as db:
        linha = db.get(LogoEmpresa, empresa_id)
        return linha.versao if linha else ""


def _resumo(e):
    """Sector e uma frase curta tirados da primeira linha da informação da empresa."""
    linha = (e.system_prompt or "").split("\n")[0].strip()
    if linha.lower().startswith((e.nome or "").lower()):
        linha = linha[len(e.nome):].lstrip(" .:-")
    m = re.match(r"\(([^)]{1,50})\)\s*\.?\s*(.*)", linha)
    sector, resto = (m.group(1), m.group(2)) if m else ("", linha)
    return sector.strip(), resto.strip()[:120]


def registar(app, exige_admin, limite_excedido, empresa_ativa, gerar_slug, exige_empresa=None):
    @app.get("/clientes")
    def pagina_clientes():
        return CLIENTES

    @app.get("/empresas")
    def pagina_empresas():
        pagamento = os.environ.get("PAGAMENTO_INSTRUCOES", "").strip() or (
            "Os dados de pagamento serão indicados pela MacTech. Contacte-nos para os receber.")
        return render_template_string(EMPRESAS, termos=TERMOS, pagamento=pagamento)

    @app.get("/api/publico/empresas")
    def listar_publico():
        """Só empresas aprovadas (pagas ou em teste dentro do prazo). Nunca mostra pendentes nem suspensas."""
        with SessionLocal() as db:
            ativas = [e for e in db.query(Empresa).filter(Empresa.slug.isnot(None)).order_by(Empresa.nome).all()
                      if empresa_ativa(e)]
            logos = {i: v for i, v in db.query(LogoEmpresa.empresa_id, LogoEmpresa.versao).all()}
            saida = []
            for e in ativas:
                sector, resumo = _resumo(e)
                saida.append({"nome": e.nome, "slug": e.slug, "logo": logos.get(e.id), "sector": sector, "resumo": resumo})
            return jsonify(empresas=saida)

    @app.get("/logo/<slug>")
    def logo_empresa(slug):
        with SessionLocal() as db:
            e = db.query(Empresa).filter_by(slug=slug).one_or_none()
            linha = db.get(LogoEmpresa, e.id) if e else None
            if not linha:
                return "", 404
            r = Response(base64.b64decode(linha.dados), mimetype=linha.tipo)
            r.headers["Cache-Control"] = "public, max-age=86400"
            r.headers["Content-Security-Policy"] = "default-src 'none'"
            return r

    @app.post("/api/publico/registar")
    def registar_empresa():
        d = request.get_json(silent=True) or {}
        if str(d.get("website") or "").strip():       # campo-armadilha: só os robôs o preenchem
            return jsonify(ok=True), 201
        if limite_excedido(("registo", request.remote_addr), 10, 3600):
            return jsonify(erro="Demasiados pedidos. Tente daqui a uma hora."), 429

        def t(campo, maximo):
            return str(d.get(campo) or "").strip()[:maximo]
        f = {"nome": t("nome", 120), "sector": t("sector", 120), "descricao": t("descricao", 1000),
             "produtos": t("produtos", 8000), "horario": t("horario", 200), "local": t("local", 300),
             "politicas": t("politicas", 1000)}
        contacto, ref = t("contacto", 120), t("ref_pagamento", 120)
        em_falta = [n for n, v in (("nome da empresa", f["nome"]), ("produtos ou serviços", f["produtos"]),
                                   ("telefone ou email", contacto), ("referência do pagamento", ref)) if not v]
        if em_falta:
            return jsonify(erro="Preencha: " + ", ".join(em_falta) + "."), 400
        if d.get("aceita_termos") is not True:
            return jsonify(erro="Tem de aceitar os termos."), 400
        logo = None
        if d.get("logo"):
            logo = _ler_logo(d.get("logo"))
            if not logo:
                return jsonify(erro="Logótipo inválido. Use uma imagem PNG, JPG ou WebP pequena."), 400
        chave, chave_hash = nova_chave_acesso()
        empresa = Empresa(nome=f["nome"], system_prompt=_prompt(d, f), humano_ativo=True, no_hub=True,
                          estado="pendente", teste_ate=None, chave_hash=chave_hash)
        with SessionLocal() as db:
            empresa.slug = gerar_slug(db, f["nome"])
            db.add(empresa)
            try:
                db.flush()
                db.add(PedidoEmpresa(empresa_id=empresa.id, contacto=contacto, ref_pagamento=ref))
                if logo:
                    _guardar_logo(db, empresa.id, logo)
                db.commit()
            except IntegrityError:
                db.rollback()
                log.exception("Não foi possível registar a empresa")
                return jsonify(erro="Não foi possível registar. Tente de novo."), 409
        log.warning("[ATENÇÃO] Novo pedido de empresa: %s (confirmar pagamento no painel)", f["nome"])
        return jsonify(ok=True, chave=chave), 201

    @app.get("/api/pedidos")
    @exige_admin
    def listar_pedidos():
        """Contacto e referência de pagamento por empresa (só o dono)."""
        with SessionLocal() as db:
            return jsonify(pedidos={p.empresa_id: {"contacto": p.contacto, "ref_pagamento": p.ref_pagamento}
                                    for p in db.query(PedidoEmpresa).all()})

    # ---------- Logótipo da empresa ----------
    @app.get("/api/logos")
    @exige_admin
    def listar_logos():
        with SessionLocal() as db:
            return jsonify(logos={i: v for i, v in db.query(LogoEmpresa.empresa_id, LogoEmpresa.versao).all()})

    def _gravar(empresa_id):
        logo = _ler_logo((request.get_json(silent=True) or {}).get("logo"))
        if not logo:
            return jsonify(erro="Logótipo inválido. Use uma imagem PNG, JPG ou WebP pequena."), 400
        with SessionLocal() as db:
            if not db.get(Empresa, empresa_id):
                return jsonify(erro="empresa não encontrada"), 404
            _guardar_logo(db, empresa_id, logo)
            db.commit()
        return jsonify(ok=True, versao=logo[2])

    def _apagar(empresa_id):
        with SessionLocal() as db:
            linha = db.get(LogoEmpresa, empresa_id)
            if linha:
                db.delete(linha)
                db.commit()
        return jsonify(ok=True)

    @app.put("/api/empresas/<int:empresa_id>/logo")
    @exige_admin
    def logo_dono_gravar(empresa_id):
        return _gravar(empresa_id)

    @app.delete("/api/empresas/<int:empresa_id>/logo")
    @exige_admin
    def logo_dono_apagar(empresa_id):
        return _apagar(empresa_id)

    if exige_empresa:
        @app.put("/api/minha/logo")
        @exige_empresa
        def logo_minha_gravar():
            if limite_excedido(("logo", g.empresa_id), 20, 3600):
                return jsonify(erro="Demasiadas alterações. Tente mais tarde."), 429
            return _gravar(g.empresa_id)

        @app.delete("/api/minha/logo")
        @exige_empresa
        def logo_minha_apagar():
            return _apagar(g.empresa_id)
