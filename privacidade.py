"""Privacidade e auditoria do MacTech (original).

- Consentimento: a primeira mensagem do cliente regista que ele aceitou continuar.
- Direito a ser esquecido: a empresa (ou o dono) pode apagar todas as mensagens e o contacto de um cliente.
- Auditoria: regista quem viu, respondeu ou apagou o quê (sem guardar o conteúdo das mensagens).

Isto não existe nos bots baratos genéricos e dá confiança às empresas angolanas.
"""
import logging
from functools import wraps

from flask import g, jsonify, request
from sqlalchemy import func

from models import Auditoria, Conversa, Mensagem, SessionLocal, agora

log = logging.getLogger("mactech.privacidade")


def registar_auditoria(db, empresa_id, ator, ator_id, acao, detalhe=None, ip=None):
    """Escreve uma linha de auditoria. Nunca falha a operação principal se o log falhar."""
    try:
        db.add(Auditoria(
            empresa_id=empresa_id,
            ator=(ator or "sistema")[:40],
            ator_id=(str(ator_id) if ator_id is not None else None) and str(ator_id)[:80],
            acao=(acao or "")[:60],
            detalhe=(detalhe or None) and str(detalhe)[:300],
            ip=(ip or None) and str(ip)[:45],
        ))
        # não faz commit aqui: quem chama é que decide
    except Exception:
        log.exception("Falha ao registar auditoria (a operação continua)")


def marcar_consentimento(conversa):
    """Na primeira mensagem do cliente, regista o consentimento (só uma vez)."""
    if conversa.consentiu_em is None:
        conversa.consentiu_em = agora()


def apagar_dados_cliente(db, conversa, ator="empresa", ator_id=None, ip=None):
    """Apaga mensagens e contacto de uma conversa. Mantém a linha da conversa (estatísticas anónimas).
    Devolve quantas mensagens foram apagadas."""
    n = db.query(Mensagem).filter_by(conversa_id=conversa.id).delete(synchronize_session=False)
    conversa.contacto = None
    conversa.inicio_historico_id = 0
    # não apaga a conversa em si para não partir estatísticas de "pessoas" antigas
    registar_auditoria(
        db, conversa.empresa_id, ator, ator_id, "apagar_cliente",
        detalhe=f"conversa {conversa.id}, {n} mensagens", ip=ip
    )
    return n


def registar(app, exige_admin, exige_empresa, iso_utc):
    """Regista as rotas de privacidade no Flask app."""

    @app.post("/api/minha/apagar-cliente")
    @exige_empresa
    def minha_apagar_cliente():
        """A empresa apaga os dados de um cliente (mensagens + contacto)."""
        d = request.get_json(silent=True) or {}
        cid = d.get("conversa_id")
        if not isinstance(cid, int):
            return jsonify(erro="conversa_id inválido"), 400
        with SessionLocal() as db:
            c = db.get(Conversa, cid)
            if not c or c.empresa_id != g.empresa_id:
                return jsonify(erro="conversa não encontrada"), 404
            n = apagar_dados_cliente(db, c, ator="empresa", ator_id=str(g.empresa_id),
                                     ip=request.remote_addr)
            db.commit()
            return jsonify(ok=True, mensagens_apagadas=n)

    @app.post("/api/conversas/<int:cid>/apagar")
    @exige_admin
    def admin_apagar_cliente(cid):
        """O dono MacTech apaga os dados de um cliente de qualquer empresa."""
        with SessionLocal() as db:
            c = db.get(Conversa, cid)
            if not c:
                return jsonify(erro="conversa não encontrada"), 404
            n = apagar_dados_cliente(db, c, ator="admin", ator_id="dono",
                                     ip=request.remote_addr)
            db.commit()
            return jsonify(ok=True, mensagens_apagadas=n)

    @app.get("/api/auditoria")
    @exige_admin
    def listar_auditoria():
        """Últimas ações registadas (só o dono vê)."""
        limite = min(int(request.args.get("limite", 50) or 50), 200)
        with SessionLocal() as db:
            linhas = (db.query(Auditoria).order_by(Auditoria.id.desc()).limit(limite).all())
            return jsonify(auditoria=[{
                "id": a.id,
                "quando": iso_utc(a.quando),
                "empresa_id": a.empresa_id,
                "ator": a.ator,
                "ator_id": a.ator_id,
                "acao": a.acao,
                "detalhe": a.detalhe,
                "ip": a.ip,
            } for a in linhas])
