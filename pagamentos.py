"""Pagamentos da MacTech: comprovativos, notificações do dono e cobrança.

Só programação: usa a base de dados e o servidor que o MacTech já tem (nada de serviços novos).
Fluxo:
  1. A empresa envia o comprovativo (ao registar-se, ou em «Minha empresa» para renovar).
  2. Cai uma notificação no painel do dono. O dono vê o comprovativo e os dados da empresa.
  3. «Já pagou» ativa a empresa por planos.DIAS_POR_MES dias (soma ao prazo se ainda estiver ativa). «Recusar» pede outro.
  4. Quando o prazo acaba (ou está a acabar) aparece uma notificação com o consumo e o texto de cobrança pronto a enviar.
As tabelas novas são criadas aqui (como em planos.py e publico.py), sem mexer no models.py.
"""
import base64
import logging
import os
import re
from datetime import timedelta, timezone
from urllib.parse import quote

from flask import g, jsonify, request
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, Conversa, Empresa, Mensagem, SessionLocal, agora, engine
import planos

log = logging.getLogger("mactech.pagamentos")

MAX_BASE64 = 1_400_000          # tamanho máximo do comprovativo em base64 (~1 MB)
MAX_BYTES = 1_050_000
MAX_PENDENTES = 3               # uma empresa não pode ter mais comprovativos à espera do que isto
AVISO_DIAS = 3                  # avisa o dono quando faltam este número de dias (ou menos)
GUARDAR_DIAS = 90               # depois de tratado, o ficheiro do comprovativo é apagado ao fim destes dias


class ProvaPagamento(Base):
    """Comprovativo de pagamento enviado por uma empresa (foto, captura ou PDF, guardado em base64)."""
    __tablename__ = "provas_pagamento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    origem: Mapped[str] = mapped_column(String(12), default="registo")     # registo | renovacao
    tipo: Mapped[str] = mapped_column(String(20))
    dados: Mapped[str] = mapped_column(Text, default="")
    referencia: Mapped[str] = mapped_column(String(120), default="")
    estado: Mapped[str] = mapped_column(String(12), default="pendente", index=True)   # pendente | aprovada | recusada
    motivo: Mapped[str] = mapped_column(String(200), default="")
    criada: Mapped[object] = mapped_column(DateTime(timezone=True), default=agora)
    decidida: Mapped[object] = mapped_column(DateTime(timezone=True), nullable=True)


def criar_tabelas():
    try:
        Base.metadata.create_all(engine)
    except Exception:
        log.exception("Não foi possível criar a tabela de comprovativos (volta a tentar no arranque da base de dados)")


criar_tabelas()

_PNG, _JPG, _PDF = b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"%PDF-"


# ---------- Lógica pura (sem base de dados; testada em testes_offline.py) ----------
def ler_prova(valor):
    """Valida um comprovativo enviado como 'data:<tipo>;base64,...'. Devolve (tipo, base64) ou None.
    Só PNG, JPEG, WebP e PDF, e o conteúdo tem de ser mesmo do tipo declarado (nunca SVG nem HTML)."""
    m = re.fullmatch(r"data:(image/png|image/jpeg|image/webp|application/pdf);base64,([A-Za-z0-9+/=]+)", str(valor or ""))
    if not m or len(m.group(2)) > MAX_BASE64:
        return None
    try:
        raw = base64.b64decode(m.group(2), validate=True)
    except Exception:
        return None
    if len(raw) > MAX_BYTES:
        return None
    tipo = m.group(1)
    certo = {"image/png": raw.startswith(_PNG), "image/jpeg": raw.startswith(_JPG), "application/pdf": raw.startswith(_PDF),
             "image/webp": raw[:4] == b"RIFF" and raw[8:12] == b"WEBP"}[tipo]
    return (tipo, m.group(2)) if certo else None


def numero_whatsapp(contacto):
    """Só dígitos, com indicativo, se o contacto parecer um telemóvel (Angola: 9 dígitos a começar por 9). Senão None."""
    texto = str(contacto or "").strip()
    if not texto or "@" in texto:
        return None
    d = re.sub(r"\D", "", texto)
    if d.startswith("00"):
        d = d[2:]
    if len(d) == 9 and d.startswith("9"):
        return "244" + d
    if len(d) == 12 and d.startswith("244"):
        return d
    if texto.startswith(("+", "00")) and 10 <= len(d) <= 15:
        return d
    return None


def link_whatsapp(contacto, texto):
    n = numero_whatsapp(contacto)
    return f"https://wa.me/{n}?text={quote(texto)}" if n else None


def instrucoes_pagamento():
    return os.environ.get("PAGAMENTO_INSTRUCOES", "").strip() or (
        "Os dados de pagamento serão indicados pela MacTech. Contacte-nos para os receber.")


def texto_cobranca(nome, plano_nome, preco_kz, consumo, instrucoes):
    linhas = [f"Olá! Aqui é a MacTech. O período de {planos.DIAS_POR_MES} dias da {nome} terminou ou está a terminar."]
    if consumo:
        linhas.append(f"Neste período o assistente atendeu {consumo['pessoas']} pessoas e recebeu {consumo['mensagens']} "
                      f"mensagens de clientes (a IA respondeu {consumo['respostas_ia']} vezes).")
    if plano_nome and preco_kz:
        linhas.append(f"Para continuar com o pacote {plano_nome}, o valor é {planos.formatar_kz(preco_kz)} Kz.")
    linhas.append(instrucoes)
    linhas.append("Depois de pagar, envie o comprovativo na área Minha empresa (ou responda a esta mensagem).")
    return "\n\n".join(linhas)


def _utc(dt):
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _iso(dt):
    dt = _utc(dt)
    return dt.astimezone(timezone.utc).isoformat() if dt else None


def avisos_de_prazo(empresas, agora_):
    """empresas: lista de {id, nome, estado, plano_ate, teste_ate, arquivada, prova_pendente}.
    Devolve [{empresa_id, tipo, dias}] com tipo 'acaba' (faltam poucos dias), 'terminou' ou 'teste_terminou'.
    Ignora empresas arquivadas e as que já têm um comprovativo à espera (o dono já está a tratar)."""
    saida = []
    for e in empresas:
        if e.get("arquivada") or e.get("prova_pendente"):
            continue
        if e["estado"] == "ativo" and e.get("plano_ate"):
            fim = _utc(e["plano_ate"])
            falta = fim - agora_
            if falta < timedelta(0):
                saida.append({"empresa_id": e["id"], "tipo": "terminou", "dias": (agora_ - fim).days})
            elif falta <= timedelta(days=AVISO_DIAS):
                saida.append({"empresa_id": e["id"], "tipo": "acaba", "dias": falta.days})
        elif e["estado"] == "teste" and e.get("teste_ate"):
            fim = _utc(e["teste_ate"])
            if fim < agora_:
                saida.append({"empresa_id": e["id"], "tipo": "teste_terminou", "dias": (agora_ - fim).days})
    return saida


# ---------- Base de dados ----------
def guardar_prova(db, empresa_id, prova, origem, referencia=""):
    db.add(ProvaPagamento(empresa_id=empresa_id, origem=origem, tipo=prova[0], dados=prova[1],
                          referencia=(referencia or "")[:120], estado="pendente"))


def marcar_tratadas(db, empresa_id):
    """Quando o dono ativa a empresa à mão, os comprovativos à espera ficam tratados (evita somar o prazo duas vezes)."""
    db.query(ProvaPagamento).filter(ProvaPagamento.empresa_id == empresa_id, ProvaPagamento.estado == "pendente") \
        .update({"estado": "aprovada", "decidida": agora()})


def consumo(db, empresa_id, desde):
    def contar(remetente):
        return (db.query(func.count(Mensagem.id)).join(Conversa, Mensagem.conversa_id == Conversa.id)
                .filter(Conversa.empresa_id == empresa_id, Mensagem.remetente == remetente,
                        Mensagem.data_hora >= desde).scalar()) or 0
    pessoas = (db.query(func.count(func.distinct(Conversa.id))).join(Mensagem, Mensagem.conversa_id == Conversa.id)
               .filter(Conversa.empresa_id == empresa_id, Mensagem.remetente == "user",
                       Mensagem.data_hora >= desde).scalar()) or 0
    return {"pessoas": pessoas, "mensagens": contar("user"), "respostas_ia": contar("assistant")}


def resumo_empresa(db, e, plano):
    """O que a empresa vê em «Minha empresa»: como pagar e em que estado está o último comprovativo."""
    ultima = db.query(ProvaPagamento).filter(ProvaPagamento.empresa_id == e.id).order_by(ProvaPagamento.id.desc()).first()
    nome = planos.PLANOS[plano]["nome"] if plano in planos.PLANOS else None
    return {"instrucoes": instrucoes_pagamento(), "pacote": nome, "preco_kz": planos.preco_de(plano), "dias": planos.DIAS_POR_MES,
            "ultima": ({"estado": ultima.estado, "motivo": ultima.motivo or "", "origem": ultima.origem,
                        "quando": _iso(ultima.criada)} if ultima else None)}


def _limpar_antigas(db):
    """Apaga só o ficheiro (a linha fica) dos comprovativos já tratados há mais de GUARDAR_DIAS dias."""
    try:
        db.query(ProvaPagamento).filter(ProvaPagamento.estado != "pendente", ProvaPagamento.dados != "",
                                        ProvaPagamento.decidida < agora() - timedelta(days=GUARDAR_DIAS)).update({"dados": ""})
        db.commit()
    except Exception:
        db.rollback()
        log.exception("Não foi possível limpar comprovativos antigos")


def registar(app, exige_admin, exige_empresa, limite_excedido, estado_de, empresa_ativa):
    import publico   # aqui dentro para não haver import circular (o publico também importa este módulo)

    def _pedido_de(db, empresa_id):
        return db.query(publico.PedidoEmpresa).filter(publico.PedidoEmpresa.empresa_id == empresa_id).first()

    # ---------- Dono ----------
    @app.get("/api/notificacoes")
    @exige_admin
    def listar_notificacoes():
        """Comprovativos à espera + empresas cujo prazo acaba ou acabou. ?resumo=1 devolve só o total (para o número no botão)."""
        so_total = request.args.get("resumo") == "1"
        with SessionLocal() as db:
            if not so_total:
                _limpar_antigas(db)
            mp = planos.mapa_planos(db)
            pend = db.query(ProvaPagamento).filter(ProvaPagamento.estado == "pendente").order_by(ProvaPagamento.id).all()
            com_prova = {p.empresa_id for p in pend}
            empresas = {e.id: e for e in db.query(Empresa).all()}
            avisos = avisos_de_prazo(
                [{"id": e.id, "nome": e.nome, "estado": estado_de(e), "plano_ate": e.plano_ate, "teste_ate": e.teste_ate,
                  "arquivada": bool(mp.get(e.id, (None, None))[1]), "prova_pendente": e.id in com_prova}
                 for e in empresas.values()], agora())
            if so_total:
                return jsonify(total=len([p for p in pend if p.empresa_id in empresas]) + len(avisos))
            pedidos = {p.empresa_id: p for p in db.query(publico.PedidoEmpresa).all()}
            provas = []
            for p in pend:
                e = empresas.get(p.empresa_id)
                if not e:
                    continue
                plano = mp.get(e.id, (None, None))[0]
                ped = pedidos.get(e.id)
                provas.append({"id": p.id, "empresa_id": e.id, "empresa": e.nome, "origem": p.origem, "tipo": p.tipo,
                               "quando": _iso(p.criada), "referencia": p.referencia or "",
                               "contacto": ped.contacto if ped else None,
                               "plano_nome": planos.PLANOS[plano]["nome"] if plano in planos.PLANOS else None,
                               "preco_kz": planos.preco_de(plano), "dias": planos.DIAS_POR_MES})
            saida = []
            for a in avisos:
                e = empresas[a["empresa_id"]]
                plano = mp.get(e.id, (None, None))[0]
                fim = _utc(e.plano_ate if a["tipo"] != "teste_terminou" else e.teste_ate)
                desde = fim - timedelta(days=planos.DIAS_POR_MES if a["tipo"] != "teste_terminou" else 30)
                ped = pedidos.get(e.id)
                saida.append({**a, "empresa": e.nome, "plano_nome": planos.PLANOS[plano]["nome"] if plano in planos.PLANOS else None,
                              "preco_kz": planos.preco_de(plano), "contacto": ped.contacto if ped else None,
                              "consumo": consumo(db, e.id, desde)})
            return jsonify(total=len(provas) + len(saida), provas=provas, avisos=saida)

    @app.get("/api/provas/<int:prova_id>")
    @exige_admin
    def ver_prova(prova_id):
        with SessionLocal() as db:
            p = db.get(ProvaPagamento, prova_id)
            if not p:
                return jsonify(erro="comprovativo não encontrado"), 404
            if not p.dados:
                return jsonify(erro="O ficheiro deste comprovativo já foi apagado (passaram mais de %d dias)." % GUARDAR_DIAS), 410
            return jsonify(tipo=p.tipo, dados=p.dados, estado=p.estado)

    @app.post("/api/provas/<int:prova_id>/aprovar")
    @exige_admin
    def aprovar_prova(prova_id):
        """«Já pagou»: ativa a empresa por DIAS_POR_MES dias (soma ao prazo se ainda estiver ativa). Corpo opcional: {"meses": 1}."""
        d = request.get_json(silent=True) or {}
        try:
            meses = max(1, min(int(d.get("meses", 1)), 12))
        except (TypeError, ValueError):
            return jsonify(erro="meses tem de ser um número"), 400
        with SessionLocal() as db:
            p = db.get(ProvaPagamento, prova_id)
            if not p:
                return jsonify(erro="comprovativo não encontrado"), 404
            if p.estado != "pendente":
                return jsonify(erro="Este comprovativo já foi tratado."), 409
            e = db.get(Empresa, p.empresa_id)
            if not e:
                return jsonify(erro="empresa não encontrada"), 404
            e.estado = "ativo"
            planos.desarquivar(db, e.id)
            fim_atual = _utc(e.plano_ate)
            base = fim_atual if fim_atual and fim_atual > agora() else agora()
            e.plano_ate = base + timedelta(days=planos.DIAS_POR_MES * meses)
            p.estado, p.decidida, p.motivo = "aprovada", agora(), ""
            db.commit()
            return jsonify(ok=True, empresa=e.nome, plano_ate=_iso(e.plano_ate))

    @app.post("/api/provas/<int:prova_id>/recusar")
    @exige_admin
    def recusar_prova(prova_id):
        d = request.get_json(silent=True) or {}
        motivo = str(d.get("motivo") or "").strip()[:200] or "Comprovativo não aceite. Envie outro, por favor."
        with SessionLocal() as db:
            p = db.get(ProvaPagamento, prova_id)
            if not p:
                return jsonify(erro="comprovativo não encontrado"), 404
            if p.estado != "pendente":
                return jsonify(erro="Este comprovativo já foi tratado."), 409
            p.estado, p.decidida, p.motivo = "recusada", agora(), motivo
            db.commit()
            return jsonify(ok=True)

    @app.get("/api/empresas/<int:empresa_id>/cobranca")
    @exige_admin
    def preparar_cobranca(empresa_id):
        """Texto de cobrança pronto a enviar (com o consumo do período) e, se o contacto for um telemóvel, o link do WhatsApp."""
        with SessionLocal() as db:
            e = db.get(Empresa, empresa_id)
            if not e:
                return jsonify(erro="empresa não encontrada"), 404
            plano = planos.plano_de(db, e.id)
            fim = _utc(e.plano_ate if estado_de(e) == "ativo" else e.teste_ate) or agora()
            c = consumo(db, e.id, fim - timedelta(days=planos.DIAS_POR_MES))
            ped = _pedido_de(db, e.id)
            nome_plano = planos.PLANOS[plano]["nome"] if plano in planos.PLANOS else None
            texto = texto_cobranca(e.nome, nome_plano, planos.preco_de(plano), c, instrucoes_pagamento())
            contacto = ped.contacto if ped else None
            return jsonify(texto=texto, contacto=contacto, link_whatsapp=link_whatsapp(contacto, texto), consumo=c)

    # ---------- Empresa ----------
    @app.post("/api/minha/prova")
    @exige_empresa
    def enviar_prova():
        """A empresa envia o comprovativo de pagamento (renovação, ou novo envio depois de recusado). Corpo: {"prova": "data:...", "referencia": ""}."""
        d = request.get_json(silent=True) or {}
        if limite_excedido(("prova", g.empresa_id), 10, 3600):
            return jsonify(erro="Demasiados envios. Tente mais tarde."), 429
        prova = ler_prova(d.get("prova"))
        if not prova:
            return jsonify(erro="Comprovativo inválido. Envie uma foto, captura de ecrã ou PDF (até 900 KB)."), 400
        with SessionLocal() as db:
            e = db.get(Empresa, g.empresa_id)
            if not e:
                return jsonify(erro="empresa não encontrada"), 404
            pendentes = db.query(func.count(ProvaPagamento.id)).filter(
                ProvaPagamento.empresa_id == e.id, ProvaPagamento.estado == "pendente").scalar() or 0
            if pendentes >= MAX_PENDENTES:
                return jsonify(erro="Já tem comprovativos à espera de confirmação. Aguarde que o dono os veja."), 429
            nome = e.nome
            guardar_prova(db, e.id, prova, "registo" if estado_de(e) == "pendente" else "renovacao", str(d.get("referencia") or ""))
            db.commit()
        log.warning("[ATENÇÃO] Comprovativo novo de %s: ver Notificações no painel", nome)
        return jsonify(ok=True), 201
