"""Páginas públicas da MacTech: início com 3 botões, lista de empresas para clientes e registo de empresas.

Só o Dono (botão "Dono" -> /painel) usa a chave de administração. Clientes e empresas nunca a veem.
Empresas que se registam sozinhas ficam 'pendentes' (invisíveis aos clientes) até o dono confirmar o
pagamento e carregar em "Ativar (pagou)" no painel."""
import logging
import os
import re

from flask import jsonify, render_template_string, request
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, Empresa, SessionLocal, agora

log = logging.getLogger("mactech.publico")


class PedidoEmpresa(Base):
    """Dados de contacto e de pagamento de uma empresa que se registou sozinha (só o dono os vê)."""
    __tablename__ = "pedidos_empresa"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    contacto: Mapped[str] = mapped_column(String(120))
    ref_pagamento: Mapped[str] = mapped_column(String(120))
    aceitou_termos_em: Mapped[object] = mapped_column(DateTime(timezone=True), default=agora)


# A tabela é criada pelo init_db() do app.py (dentro de um try), para um problema na base nunca fechar o site.

TERMOS = """MODELO DE TERMOS (o dono deve rever e adaptar com um advogado antes de usar com clientes reais)

1. Serviço: a MacTech fornece um assistente de atendimento com inteligência artificial, que responde a clientes da empresa por chat e/ou WhatsApp com base nas informações que a empresa fornece.
2. Informação da empresa: a empresa é responsável pela exactidão e actualização das informações (produtos, preços, horários). O assistente usa apenas essas informações, mas pode cometer erros; a empresa deve acompanhar as conversas.
3. Pagamento: o serviço é activado depois de a MacTech confirmar o pagamento inicial. Sem pagamento confirmado, a empresa não aparece aos clientes.
4. Teste: as empresas abordadas pela MacTech podem ter um período de teste gratuito de 1 dia.
5. Dados: as conversas entre clientes e o assistente são guardadas para prestar o serviço e melhorar o atendimento. A empresa deve informar os seus clientes disso.
6. Suspensão: a MacTech pode suspender o serviço por falta de pagamento, uso abusivo ou conteúdo ilegal.
7. Limites: o serviço pode ficar indisponível por falhas técnicas ou dos fornecedores de IA, sem que isso dê direito a indemnização."""

# ---------- páginas ----------
BASE_CSS = """<meta name="theme-color" content="#0b1f3a"><style>
:root{--bg:#f3f6fb;--card:#fff;--ink:#0b1f3a;--mut:#58677d;--acc:#0f9d58;--line:#e1e8f0;--soft:#e6f6ee;--shadow:0 10px 28px rgba(11,31,58,.08)}
@media(prefers-color-scheme:dark){:root{--bg:#07121f;--card:#0f2036;--ink:#e8eef6;--mut:#9db0c6;--acc:#2fcf7a;--line:#1c3350;--soft:#0f3a2c;--shadow:none}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--acc)}.wrap{max-width:1040px;margin:0 auto;padding:0 18px}.page{max-width:620px;margin:0 auto;padding:16px 18px 40px}
.nav{display:flex;align-items:center;justify-content:space-between;padding:14px 0}
.logo{font-weight:800;font-size:22px;letter-spacing:-.02em;color:inherit;text-decoration:none}.logo span{color:var(--acc)}
.nav a.mini{color:inherit;text-decoration:none;font-size:14px;font-weight:600;border:1px solid var(--line);border-radius:999px;padding:6px 14px}
.hero{background:linear-gradient(135deg,#0b1f3a 0%,#123a63 55%,#0f7a55 135%);color:#fff;padding-bottom:54px}
.hero .logo{color:#fff}.hero .mini{border-color:rgba(255,255,255,.35)!important}
.hero h1{font-size:clamp(30px,6.5vw,52px);line-height:1.08;margin:34px 0 14px;letter-spacing:-.03em;max-width:15em}
.hero p{font-size:clamp(16px,2.4vw,19px);color:#cfe0f1;max-width:34em;margin:0 0 24px}
.cta{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--acc);color:#fff;border:0;border-radius:12px;padding:14px 22px;font:700 16px system-ui,sans-serif;text-decoration:none;cursor:pointer;box-shadow:0 6px 16px rgba(15,157,88,.28);transition:transform .15s}
.btn:hover{transform:translateY(-1px)}.btn.alt{background:transparent;color:inherit;border:1.5px solid currentColor;box-shadow:none}.hero .btn.alt{color:#fff;border-color:rgba(255,255,255,.55)}
.btn.full{width:100%;margin-top:14px}.btn:focus-visible,a:focus-visible,input:focus-visible,textarea:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}.chip{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:5px 12px;font-size:13px}
.sec{padding:42px 0 4px}.sec h2{font-size:26px;letter-spacing:-.02em;margin:0 0 6px}.sub{color:var(--mut);margin:0 0 20px}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin:12px 0;box-shadow:var(--shadow)}.grid .card{margin:0}
a.card{display:block;color:inherit;text-decoration:none;transition:transform .15s,border-color .15s}a.card:hover{transform:translateY(-3px);border-color:var(--acc)}
.ico{width:46px;height:46px;border-radius:12px;background:var(--soft);display:grid;place-items:center;font-size:23px;margin-bottom:10px}
.card h3{margin:0 0 4px;font-size:18px}.card p{margin:0;color:var(--mut);font-size:15px}
.num{width:34px;height:34px;border-radius:50%;background:var(--acc);color:#fff;display:grid;place-items:center;font-weight:800;margin-bottom:10px}
.foot{padding:34px 0 40px;color:var(--mut);font-size:14px;text-align:center}
h1.t{font-size:30px;letter-spacing:-.02em;margin:8px 0 4px}.lead{color:var(--mut);margin:0 0 14px}.back{display:inline-block;margin:6px 0;text-decoration:none;font-weight:600}
label{display:block;margin-top:12px;font-weight:600;font-size:14px}
input,textarea{width:100%;border:1.5px solid var(--line);border-radius:12px;padding:12px;font:16px system-ui,sans-serif;background:var(--bg);color:var(--ink)}
input[type=checkbox]{width:auto}.check{display:flex;gap:8px;align-items:center;font-weight:500}
.msg{min-height:1.4em;margin:10px 0 0}.erro{color:#d93025;font-weight:600}.ok{color:var(--acc);font-weight:600}
pre{white-space:pre-wrap;font:14px/1.5 system-ui,sans-serif;margin:8px 0 0;color:var(--mut)}summary{cursor:pointer;font-weight:600;color:var(--acc)}
.emp{display:flex;align-items:center;gap:14px}.av{width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#0b1f3a,#0f9d58);color:#fff;display:grid;place-items:center;font-weight:800;font-size:20px;flex:none}
.emp b{font-size:17px;display:block}.emp small{color:var(--mut)}.emp .go{margin-left:auto;color:var(--acc);font-weight:700}
.h{position:absolute;left:-9999px}
</style>"""


def _topo(rotulo_botao="Dono", destino="/painel"):
    return ('<div class="nav"><a class="logo" href="/">Mac<span>Tech</span></a>'
            f'<a class="mini" href="{destino}">{rotulo_botao}</a></div>')


INICIO = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MacTech · Atendimento com IA para empresas</title>""" + BASE_CSS + """</head><body>
<header class="hero"><div class="wrap">""" + _topo() + """
<h1>Atenda os seus clientes 24 horas por dia, com inteligência artificial</h1>
<p>A MacTech responde às perguntas dos clientes da sua empresa em segundos, só com a informação que você forneceu, e passa a uma pessoa quando for preciso.</p>
<div class="cta"><a class="btn" href="/clientes">Sou cliente: fazer uma pergunta</a><a class="btn alt" href="/empresas">Registar a minha empresa</a></div>
<div class="chips"><span class="chip">Sem instalar nada</span><span class="chip">Em português</span><span class="chip">Chat no site</span><span class="chip">Passa a atendente humano</span></div>
</div></header>
<main class="wrap">
<section class="sec"><h2>Escolha o seu acesso</h2><p class="sub">Cada pessoa entra pelo seu botão.</p>
<div class="grid">
<a class="card" href="/clientes"><div class="ico">💬</div><h3>Cliente</h3><p>Escolha a empresa e faça as suas perguntas. Não precisa de conta nem de código.</p></a>
<a class="card" href="/empresas"><div class="ico">🏢</div><h3>Empresa</h3><p>Registe a sua empresa, leia os termos, faça o pagamento inicial e ative o seu assistente.</p></a>
<a class="card" href="/painel"><div class="ico">🔐</div><h3>Dono</h3><p>Área reservada ao dono da MacTech, para aprovar empresas e ver as conversas.</p></a>
</div></section>
<section class="sec"><h2>Como funciona</h2><p class="sub">Em três passos.</p>
<div class="grid">
<div class="card"><div class="num">1</div><h3>A empresa regista-se</h3><p>Indica produtos, preços, horário e contactos.</p></div>
<div class="card"><div class="num">2</div><h3>O assistente aprende</h3><p>Responde só com a informação da empresa, sem inventar preços nem prazos.</p></div>
<div class="card"><div class="num">3</div><h3>Os clientes perguntam</h3><p>Recebem respostas na hora. Se for preciso, uma pessoa assume a conversa.</p></div>
</div></section>
<section class="sec"><h2>O que a sua empresa ganha</h2><p class="sub">Menos mensagens repetidas, mais vendas.</p>
<div class="grid">
<div class="card"><div class="ico">⏱️</div><h3>Respostas imediatas</h3><p>Dia e noite, sem fila de espera.</p></div>
<div class="card"><div class="ico">🙋</div><h3>Atendimento humano</h3><p>Reclamações e pedidos especiais passam a uma pessoa da equipa.</p></div>
<div class="card"><div class="ico">📇</div><h3>Contactos de interessados</h3><p>Guarda o nome e o telefone de quem quer comprar.</p></div>
<div class="card"><div class="ico">❓</div><h3>Perguntas sem resposta</h3><p>Veja o que os clientes perguntam e a IA ainda não sabe.</p></div>
<div class="card"><div class="ico">📊</div><h3>Painel com números</h3><p>Visitas, mensagens e conversas num só sítio.</p></div>
<div class="card"><div class="ico">📱</div><h3>Chat e WhatsApp</h3><p>Link de chat para partilhar e ligação opcional ao WhatsApp.</p></div>
</div></section>
<div class="foot">{% if whatsapp %}<a class="btn" href="{{ whatsapp }}">Falar com a MacTech no WhatsApp</a><br><br>{% endif %}MacTech · Angola</div>
</main></body></html>"""

CLIENTES = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MacTech · Escolha a empresa</title>""" + BASE_CSS + """</head><body><div class="page">
""" + _topo("Início", "/") + """
<h1 class="t">Com quem quer falar?</h1><p class="lead">Escolha a empresa e faça a sua pergunta.</p>
<input id="q" placeholder="Procurar empresa" aria-label="Procurar empresa" autocomplete="off">
<div id="lista"></div><p id="vazio" class="msg lead">A carregar empresas...</p>
<script>
var todas = [];
function mostrar() {
  var q = document.getElementById('q').value.toLowerCase(), L = document.getElementById('lista');
  L.textContent = '';
  var f = todas.filter(function (e) { return e.nome.toLowerCase().indexOf(q) >= 0; });
  f.forEach(function (e) {
    var a = document.createElement('a'); a.className = 'card emp'; a.href = '/c/' + encodeURIComponent(e.slug);
    var av = document.createElement('div'); av.className = 'av'; av.textContent = e.nome.charAt(0).toUpperCase();
    var d = document.createElement('div'), b = document.createElement('b'), s = document.createElement('small');
    b.textContent = e.nome; s.textContent = 'Assistente disponível agora'; d.appendChild(b); d.appendChild(s);
    var g = document.createElement('span'); g.className = 'go'; g.textContent = 'Falar →';
    a.appendChild(av); a.appendChild(d); a.appendChild(g); L.appendChild(a);
  });
  document.getElementById('vazio').textContent = f.length ? '' : (todas.length ? 'Nenhuma empresa encontrada.' : 'Ainda não há empresas disponíveis.');
}
fetch('/api/publico/empresas').then(function (r) { return r.json(); }).then(function (j) { todas = j.empresas || []; mostrar(); })
  .catch(function () { document.getElementById('vazio').textContent = 'Não foi possível carregar a lista. Tente de novo.'; });
document.getElementById('q').oninput = mostrar;
</script></div></body></html>"""

EMPRESAS = """<!DOCTYPE html><html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>MacTech · Registar empresa</title>""" + BASE_CSS + """</head><body><div class="page">
""" + _topo("Início", "/") + """
<h1 class="t">Registe a sua empresa</h1><p class="lead">Três passos. A sua empresa fica visível aos clientes assim que o pagamento for confirmado.</p>
<div class="card"><div class="num">1</div><h3>Termos</h3><details><summary>Ler os termos</summary><pre>{{ termos }}</pre></details></div>
<div class="card"><div class="num">2</div><h3>Pagamento inicial</h3><pre>{{ pagamento }}</pre></div>
<form id="f" class="card"><div class="num">3</div><h3>Dados da empresa</h3>
<label for="n">Nome da empresa</label><input id="n" maxlength="120" required>
<label for="s">Sector (ex.: loja de tecnologia, clínica)</label><input id="s" maxlength="120">
<label for="d">O que a empresa faz</label><textarea id="d" rows="2" maxlength="1000"></textarea>
<label for="p">Produtos ou serviços (um por linha, com preços e detalhes)</label><textarea id="p" rows="5" maxlength="8000" required></textarea>
<label for="h">Horário</label><input id="h" maxlength="200">
<label for="l">Contactos e localização</label><input id="l" maxlength="300">
<label for="g">Garantia, entrega e pagamento</label><textarea id="g" rows="2" maxlength="1000"></textarea>
<label for="c">O seu telefone ou email (só a MacTech vê)</label><input id="c" maxlength="120" required>
<label for="r">Referência ou comprovativo do pagamento</label><input id="r" maxlength="120" required>
<input class="h" id="w" tabindex="-1" autocomplete="off" aria-hidden="true">
<label class="check"><input type="checkbox" id="t"> Li e aceito os termos</label>
<button class="btn full" type="submit">Enviar pedido</button>
<p id="m" class="msg"></p></form>
{% if whatsapp %}<p class="lead">Dúvidas? <a href="{{ whatsapp }}">Fale connosco no WhatsApp</a>.</p>{% endif %}
<script>
function v(i) { return document.getElementById(i).value.trim(); }
document.getElementById('f').onsubmit = function (ev) {
  ev.preventDefault();
  var m = document.getElementById('m'); m.className = 'msg'; m.textContent = 'A enviar...';
  fetch('/api/publico/registar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
    nome: v('n'), sector: v('s'), descricao: v('d'), produtos: v('p'), horario: v('h'), local: v('l'), politicas: v('g'),
    contacto: v('c'), ref_pagamento: v('r'), aceita_termos: document.getElementById('t').checked, website: v('w') }) })
    .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
    .then(function (x) {
      if (x.ok) { m.className = 'msg ok'; m.textContent = 'Pedido enviado. Assim que o pagamento for confirmado, a sua empresa fica disponível aos clientes.'; document.getElementById('f').reset(); }
      else { m.className = 'msg erro'; m.textContent = x.j.erro || 'Não foi possível enviar.'; }
    }).catch(function () { m.className = 'msg erro'; m.textContent = 'Sem ligação. Tente de novo.'; });
};
</script></div></body></html>"""


def _whatsapp():
    """Botão opcional 'Falar com a MacTech': variável CONTACTO_WHATSAPP (só números, com indicativo, ex. 244923000000)."""
    n = re.sub(r"\D", "", os.environ.get("CONTACTO_WHATSAPP", ""))
    return f"https://wa.me/{n}" if len(n) >= 9 else ""


def pagina_inicio():
    return render_template_string(INICIO, whatsapp=_whatsapp())


def _prompt(d, f):
    """Mesmo formato do formulário do painel."""
    linhas = [l.strip() for l in f["produtos"].split("\n") if l.strip()]
    return (f["nome"] + (f" ({f['sector']})" if f["sector"] else "") + ". " + f["descricao"] + "\nProdutos e serviços:\n"
            + "\n".join("- " + l for l in linhas)
            + (f"\nHorário: {f['horario']}" if f["horario"] else "")
            + (f"\nContactos e localização: {f['local']}" if f["local"] else "")
            + (f"\nGarantia, entrega e pagamento: {f['politicas']}" if f["politicas"] else ""))


def registar(app, exige_admin, limite_excedido, empresa_ativa, gerar_slug):
    @app.get("/clientes")
    def pagina_clientes():
        return CLIENTES

    @app.get("/empresas")
    def pagina_empresas():
        pagamento = os.environ.get("PAGAMENTO_INSTRUCOES", "").strip() or (
            "Os dados de pagamento serão indicados pela MacTech. Contacte-nos para os receber.")
        return render_template_string(EMPRESAS, termos=TERMOS, pagamento=pagamento, whatsapp=_whatsapp())

    @app.get("/api/publico/empresas")
    def listar_publico():
        """Só empresas aprovadas (pagas ou em teste dentro do prazo). Nunca mostra pendentes nem suspensas."""
        with SessionLocal() as db:
            ativas = [e for e in db.query(Empresa).filter(Empresa.slug.isnot(None)).order_by(Empresa.nome).all()
                      if empresa_ativa(e)]
            return jsonify(empresas=[{"nome": e.nome, "slug": e.slug} for e in ativas])

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
        empresa = Empresa(nome=f["nome"], system_prompt=_prompt(d, f), humano_ativo=True, no_hub=True,
                          estado="pendente", teste_ate=None)
        with SessionLocal() as db:
            empresa.slug = gerar_slug(db, f["nome"])
            db.add(empresa)
            try:
                db.flush()
                db.add(PedidoEmpresa(empresa_id=empresa.id, contacto=contacto, ref_pagamento=ref))
                db.commit()
            except IntegrityError:
                db.rollback()
                log.exception("Não foi possível registar a empresa")
                return jsonify(erro="Não foi possível registar. Tente de novo."), 409
        log.warning("[ATENÇÃO] Novo pedido de empresa: %s (confirmar pagamento no painel)", f["nome"])
        return jsonify(ok=True), 201

    @app.get("/api/pedidos")
    @exige_admin
    def listar_pedidos():
        """Contacto e referência de pagamento por empresa (só o dono)."""
        with SessionLocal() as db:
            return jsonify(pedidos={p.empresa_id: {"contacto": p.contacto, "ref_pagamento": p.ref_pagamento}
                                    for p in db.query(PedidoEmpresa).all()})
