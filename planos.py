"""Módulo de manutenção da MacTech: pacotes, uso e custo da IA, lucro e eliminação de empresas.

Só programação: usa a base de dados e a IA que o MacTech já tem. Não mexe no visual nem no models.py
(as tabelas novas são criadas aqui, como no publico.py).

Para mudar preços, limites ou custos, edita só as constantes aqui em baixo.
"""
import logging

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped, mapped_column

from models import Base, SessionLocal, agora, engine

log = logging.getLogger("mactech.planos")

# ---------- Pacotes (edita aqui os preços e os limites) ----------
PLANOS = {
    "basico": {
        "nome": "Básico", "preco_kz": 25000, "mensagens_mes": 600, "whatsapp": False, "ferramentas": False,
        "resumo": "Chat no site, 600 mensagens de clientes por mês e painel de conversas.",
    },
    "profissional": {
        "nome": "Profissional", "preco_kz": 55000, "mensagens_mes": 3000, "whatsapp": True, "ferramentas": False,
        "resumo": "Chat e WhatsApp, 3.000 mensagens por mês e passagem para uma pessoa da equipa.",
    },
    "empresarial": {
        "nome": "Empresarial", "preco_kz": 120000, "mensagens_mes": 12000, "whatsapp": True, "ferramentas": True,
        "resumo": "Tudo incluído: stock, encomendas, faturas e departamentos, com 12.000 mensagens por mês.",
    },
}

# ---------- Custos (estimativas editáveis; servem para calcular o lucro) ----------
CUSTO_FIXO_MENSAL_KZ = 20000        # servidor e base de dados no Render, por mês (estimativa)
CUSTO_IA_KZ_MIL_ENTRADA = 0.10      # Kz por cada 1000 tokens que a IA lê (estimativa)
CUSTO_IA_KZ_MIL_SAIDA = 0.40        # Kz por cada 1000 tokens que a IA escreve (estimativa)
AVISO_PERCENTAGEM = 80              # avisa quando a empresa já gastou 80% do limite mensal
HORAS_ATE_IA_RETOMAR = 6            # se uma pessoa assumiu a conversa e ninguém responde há tanto tempo, a IA volta a atender
DIAS_POR_MES = 31                   # cada pagamento confirmado dá estes dias de uso (soma ao prazo se renovar antes do fim)


class PlanoEmpresa(Base):
    """Pacote de cada empresa e, se foi arquivada, desde quando."""
    __tablename__ = "planos_empresa"
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), primary_key=True)
    plano: Mapped[str] = mapped_column(String(20), nullable=True)
    arquivada_em: Mapped[object] = mapped_column(DateTime(timezone=True), nullable=True)


class UsoIA(Base):
    """Quanto a IA trabalhou por empresa e por mês (para calcular o custo)."""
    __tablename__ = "uso_ia"
    __table_args__ = (UniqueConstraint("empresa_id", "mes", name="uq_uso_empresa_mes"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    mes: Mapped[str] = mapped_column(String(7), index=True)
    chamadas: Mapped[int] = mapped_column(Integer, default=0)
    entrada: Mapped[int] = mapped_column(Integer, default=0)
    saida: Mapped[int] = mapped_column(Integer, default=0)


def criar_tabelas():
    """Cria só as tabelas novas, se ainda não existirem. Nunca derruba o site se a base de dados estiver em baixo."""
    try:
        Base.metadata.create_all(engine)
    except Exception:
        log.exception("Não foi possível criar as tabelas de pacotes e uso (volta a tentar no arranque da base de dados)")


criar_tabelas()


# ---------- Lógica pura (sem base de dados) ----------
def plano_valido(chave):
    return chave if chave in PLANOS else None


def limite_de(chave):
    """Mensagens de clientes por mês permitidas. None = sem limite (empresas antigas, sem pacote)."""
    return PLANOS[chave]["mensagens_mes"] if chave in PLANOS else None


def preco_de(chave):
    return PLANOS[chave]["preco_kz"] if chave in PLANOS else 0


def formatar_kz(valor):
    return f"{int(round(valor)):,}".replace(",", ".")


def permite(db, empresa_id, recurso):
    """recurso: 'whatsapp' ou 'ferramentas'. Empresas sem pacote (contas antigas) têm tudo."""
    plano = plano_de(db, empresa_id)
    return True if plano not in PLANOS else bool(PLANOS[plano].get(recurso))


def lista_publica():
    """Pacotes para mostrar no registo: [(chave, {nome, preco, resumo, mensagens})]."""
    return [(k, {"nome": p["nome"], "preco": formatar_kz(p["preco_kz"]), "resumo": p["resumo"],
                 "mensagens": formatar_kz(p["mensagens_mes"])}) for k, p in PLANOS.items()]


def custo_ia_kz(entrada, saida):
    return (entrada or 0) / 1000 * CUSTO_IA_KZ_MIL_ENTRADA + (saida or 0) / 1000 * CUSTO_IA_KZ_MIL_SAIDA


def estado_do_limite(usado, limite):
    """'sem_limite', 'ok', 'perto' (>= 80%) ou 'atingido'."""
    if not limite:
        return "sem_limite"
    if usado > limite:
        return "atingido"
    if usado * 100 >= limite * AVISO_PERCENTAGEM:
        return "perto"
    return "ok"


def analisar(linhas, custo_fixo=None):
    """Junta as linhas por empresa e calcula os totais e o lucro.
    Cada linha: {receita_kz, custo_ia_kz, respostas_ia, ativa}. Devolve o dicionário de totais."""
    fixo = CUSTO_FIXO_MENSAL_KZ if custo_fixo is None else custo_fixo
    receita = sum(l["receita_kz"] for l in linhas)
    custo_ia = sum(l["custo_ia_kz"] for l in linhas)
    respostas = sum(l["respostas_ia"] for l in linhas)
    lucro = receita - custo_ia - fixo
    return {
        "receita_kz": round(receita), "custo_ia_kz": round(custo_ia, 2), "custo_fixo_kz": round(fixo),
        "lucro_kz": round(lucro), "margem_pct": round(lucro * 100 / receita) if receita else 0,
        "empresas_ativas": sum(1 for l in linhas if l["ativa"]), "respostas_ia": respostas,
        "custo_por_resposta_kz": round(custo_ia / respostas, 3) if respostas else 0,
    }


def mes_atual():
    return agora().strftime("%Y-%m")


def inicio_do_mes():
    return agora().replace(day=1, hour=0, minute=0, second=0, microsecond=0)


# ---------- Base de dados ----------
def definir_plano(db, empresa_id, plano):
    linha = db.get(PlanoEmpresa, empresa_id)
    if linha:
        linha.plano = plano
    else:
        db.add(PlanoEmpresa(empresa_id=empresa_id, plano=plano))


def plano_de(db, empresa_id):
    linha = db.get(PlanoEmpresa, empresa_id)
    return linha.plano if linha else None


def arquivada_em(db, empresa_id):
    linha = db.get(PlanoEmpresa, empresa_id)
    return linha.arquivada_em if linha else None


def arquivar(db, empresa_id):
    linha = db.get(PlanoEmpresa, empresa_id)
    if not linha:
        linha = PlanoEmpresa(empresa_id=empresa_id, plano=None)
        db.add(linha)
    linha.arquivada_em = agora()


def desarquivar(db, empresa_id):
    linha = db.get(PlanoEmpresa, empresa_id)
    if linha:
        linha.arquivada_em = None


def mapa_planos(db):
    """{empresa_id: (plano, arquivada_em)}"""
    return {l.empresa_id: (l.plano, l.arquivada_em) for l in db.query(PlanoEmpresa).all()}


def mapa_uso(db, mes=None):
    """{empresa_id: (chamadas, entrada, saida)} do mês."""
    mes = mes or mes_atual()
    return {l.empresa_id: (l.chamadas or 0, l.entrada or 0, l.saida or 0)
            for l in db.query(UsoIA).filter_by(mes=mes).all()}


def registar_uso(empresa_id, entrada, saida):
    """Soma uma chamada à IA ao uso do mês. Nunca deixa um erro daqui estragar a resposta ao cliente."""
    if not (entrada or saida):
        return
    mes = mes_atual()
    for _ in range(2):   # 2.ª tentativa: duas respostas ao mesmo tempo podem criar a linha do mês em simultâneo
        try:
            with SessionLocal() as db:
                linha = db.query(UsoIA).filter_by(empresa_id=empresa_id, mes=mes).one_or_none()
                if linha:
                    linha.chamadas = (linha.chamadas or 0) + 1
                    linha.entrada = (linha.entrada or 0) + int(entrada or 0)
                    linha.saida = (linha.saida or 0) + int(saida or 0)
                else:
                    db.add(UsoIA(empresa_id=empresa_id, mes=mes, chamadas=1,
                                 entrada=int(entrada or 0), saida=int(saida or 0)))
                db.commit()
                return
        except IntegrityError:
            continue
        except Exception:
            log.exception("Não foi possível registar o uso da IA")
            return


# ---------- Eliminar uma empresa e tudo o que depende dela ----------
def eliminar_dados_empresa(db, metadata, tabela_empresa, empresa_id):
    """Apaga a empresa e tudo o que depende dela (conversas, mensagens, tickets, logótipo, pacote...).
    Segue as ligações (chaves estrangeiras) declaradas nos modelos, por isso apanha também as tabelas do
    nível 4. Corre dentro da transação de quem chama: se algo falhar, quem chama faz rollback e nada se perde.
    Devolve {tabela: linhas apagadas}."""
    tabelas = {t.name: t for t in metadata.sorted_tables}
    raiz = tabelas[tabela_empresa]
    pk_raiz = list(raiz.primary_key.columns)[0].name
    pais = {}   # filho -> [(pai, coluna do filho, coluna do pai)]
    for t in tabelas.values():
        for fk in t.foreign_keys:
            pai = fk.column.table.name
            if pai != t.name:
                pais.setdefault(t.name, []).append((pai, fk.parent.name, fk.column.name))

    def onde(nome, visitando):
        if nome == tabela_empresa:
            return f'"{pk_raiz}" = :eid'
        if nome in visitando:
            return None
        partes = []
        for pai, col_filho, col_pai in pais.get(nome, []):
            sub = onde(pai, visitando | {nome})
            if sub:
                partes.append(f'"{col_filho}" IN (SELECT "{col_pai}" FROM "{pai}" WHERE {sub})')
        return "(" + " OR ".join(partes) + ")" if partes else None

    def fundo(nome, visitando=frozenset()):
        """Distância à empresa pelo caminho mais longo (os mais fundos apagam-se primeiro)."""
        if nome == tabela_empresa:
            return 0
        if nome in visitando:
            return -1
        distancias = [fundo(pai, visitando | {nome}) for pai, _, _ in pais.get(nome, [])]
        distancias = [d for d in distancias if d >= 0]
        return 1 + max(distancias) if distancias else -1

    alvos = []
    for nome in tabelas:
        d = fundo(nome)
        cond = onde(nome, frozenset())
        if d >= 0 and cond:
            alvos.append((d, nome, cond))
    apagadas = {}
    for _, nome, cond in sorted(alvos, key=lambda x: -x[0]):
        resultado = db.execute(text(f'DELETE FROM "{nome}" WHERE {cond}'), {"eid": empresa_id})
        apagadas[nome] = getattr(resultado, "rowcount", 0)
    return apagadas
