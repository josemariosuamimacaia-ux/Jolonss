"""Base de dados (SQLite ou PostgreSQL via SQLAlchemy): empresas, conversas e mensagens."""
import importlib.util
import logging
from urllib.parse import parse_qs, urlsplit, urlunsplit
from datetime import datetime, timedelta, timezone

from sqlalchemy import (Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint,
                        create_engine, event, inspect, text)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker)

from config import cfg

log = logging.getLogger("mactech.db")

_sqlite = cfg.database_url.startswith("sqlite")


def preparar_url(url: str, usar_psycopg2: bool):
    """Devolve (url, connect_args). Para PostgreSQL usa o pg8000 (Python puro: instala em qualquer versão do Python,
    ao contrário do psycopg2, que precisa de ficheiros compilados). O pg8000 não entende ?sslmode=..., por isso
    esse parâmetro vira ssl_context (o Neon exige ligação segura)."""
    if url.startswith("sqlite"):
        return url, {"timeout": 30}
    p = urlsplit(url)
    if p.scheme in ("postgresql", "postgres"):
        if usar_psycopg2:
            return url, {"connect_timeout": 10}
        sslmode = (parse_qs(p.query).get("sslmode") or [""])[0].lower()
        args = {"timeout": 10}
        if sslmode in ("require", "verify-ca", "verify-full") or (p.hostname or "").endswith(".neon.tech"):
            args["ssl_context"] = True
        return urlunsplit(("postgresql+pg8000", p.netloc, p.path, "", "")), args
    return url, {}


URL_ERRO = None
URL_INVALIDA = False   # True se o DATABASE_URL estiver mal escrito (o site arranca e mostra um aviso, em vez de fechar)
try:
    _url, _args = preparar_url(cfg.database_url, importlib.util.find_spec("pg8000") is None)   # pg8000 sempre que estiver instalado
    engine = create_engine(_url, pool_pre_ping=True, connect_args=_args)
except Exception as _e:
    log.exception("DATABASE_URL inválido ou driver em falta (tem de começar por postgresql://)")
    URL_INVALIDA = True
    URL_ERRO = _e
    _sqlite = True
    engine = create_engine("sqlite:///mactech.db")   # só para o site conseguir arrancar; não é usado enquanto o URL estiver inválido

if _sqlite:
    @event.listens_for(engine, "connect")
    def _pragmas(con, _):
        """WAL permite ler e escrever ao mesmo tempo sem 'database is locked'."""
        cur = con.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        cur.close()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def agora():
    return datetime.now(timezone.utc)


def fim_teste():
    """O teste grátis dura 1 dia a partir do registo."""
    return agora() + timedelta(days=1)


class Base(DeclarativeBase):
    pass


class Empresa(Base):
    """Um cliente da MacTech. Cada empresa tem o seu catálogo e, opcionalmente, o seu número de WhatsApp."""
    __tablename__ = "empresas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    slug: Mapped[str | None] = mapped_column(String(60), unique=True, index=True, nullable=True)  # endereço do chat web
    wa_phone_number_id: Mapped[str | None] = mapped_column(String(40), unique=True, index=True, nullable=True)
    wa_access_token: Mapped[str | None] = mapped_column(Text, nullable=True)  # TODO: cifrar em produção
    system_prompt: Mapped[str] = mapped_column(Text)     # catálogo + regras do negócio
    humano_ativo: Mapped[bool] = mapped_column(Boolean, default=True)  # a empresa tem equipa para atender?
    no_hub: Mapped[bool] = mapped_column(Boolean, default=True)        # aparece na lista do número partilhado?
    estado: Mapped[str] = mapped_column(String(10), default="teste")   # 'pendente', 'teste', 'ativo' ou 'suspenso'
    teste_ate: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=fim_teste)
    # Nível 4: ferramentas que a IA pode usar ("stock,encomendas,fatura,departamentos") e ligação ao sistema da empresa
    ferramentas: Mapped[str | None] = mapped_column(Text, nullable=True)
    integracao_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    integracao_segredo: Mapped[str | None] = mapped_column(Text, nullable=True)


class Conversa(Base):
    """Uma conversa entre um cliente (número ou sessão web) e uma empresa."""
    __tablename__ = "conversas"
    __table_args__ = (UniqueConstraint("phone_number_id", "cliente_numero"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number_id: Mapped[str] = mapped_column(String(40), index=True)  # número que recebeu a conversa ('web' no chat web)
    empresa_id: Mapped[int | None] = mapped_column(ForeignKey("empresas.id"), index=True, nullable=True)
    cliente_numero: Mapped[str] = mapped_column(String(64))
    humano_assumiu: Mapped[bool] = mapped_column(Boolean, default=False)  # True = a IA fica calada
    inicio_historico_id: Mapped[int] = mapped_column(Integer, default=0)  # a IA só vê mensagens depois deste id
    contacto: Mapped[str | None] = mapped_column(String(120), nullable=True)  # telefone/email do cliente
    departamento_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # para onde a IA a encaminhou
    agente_id: Mapped[int | None] = mapped_column(Integer, nullable=True)        # atendente humano que a assumiu
    mensagens: Mapped[list["Mensagem"]] = relationship(back_populates="conversa")


class Mensagem(Base):
    __tablename__ = "mensagens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversa_id: Mapped[int] = mapped_column(ForeignKey("conversas.id"), index=True)
    remetente: Mapped[str] = mapped_column(String(10))  # 'user', 'assistant' ou 'human'
    conteudo: Mapped[str] = mapped_column(Text)
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)
    wa_id: Mapped[str | None] = mapped_column(String(80), index=True, nullable=True)  # id da mensagem no WhatsApp (evita duplicados)
    sem_resposta: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)  # pergunta que o bot não soube responder
    conversa: Mapped[Conversa] = relationship(back_populates="mensagens")


class Departamento(Base):
    """Vendas, Suporte, Financeiro... A IA encaminha o cliente para o departamento certo."""
    __tablename__ = "departamentos"
    __table_args__ = (UniqueConstraint("empresa_id", "nome"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    nome: Mapped[str] = mapped_column(String(60))
    descricao: Mapped[str | None] = mapped_column(String(200), nullable=True)


class Agente(Base):
    """Atendente humano. Entra em /agente com a sua chave (guardada só em hash)."""
    __tablename__ = "agentes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    nome: Mapped[str] = mapped_column(String(80))
    chave_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    departamento_id: Mapped[int | None] = mapped_column(Integer, nullable=True)  # vazio = vê todos
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class Produto(Base):
    """Catálogo com preço e stock (a alternativa a ligar um ERP)."""
    __tablename__ = "produtos"
    __table_args__ = (UniqueConstraint("empresa_id", "sku"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    sku: Mapped[str] = mapped_column(String(40))
    nome: Mapped[str] = mapped_column(String(160))
    preco: Mapped[float | None] = mapped_column(Float, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0)


class Encomenda(Base):
    __tablename__ = "encomendas"
    __table_args__ = (UniqueConstraint("empresa_id", "codigo"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    codigo: Mapped[str] = mapped_column(String(40))
    contacto: Mapped[str] = mapped_column(String(120))   # telefone ou email do dono da encomenda
    estado: Mapped[str] = mapped_column(String(60))
    itens: Mapped[str | None] = mapped_column(Text, nullable=True)
    total: Mapped[float | None] = mapped_column(Float, nullable=True)
    atualizado: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)


class Ticket(Base):
    """Pedido registado para a equipa (reclamação, pedido de fatura, transferência)."""
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    conversa_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    departamento: Mapped[str | None] = mapped_column(String(60), nullable=True)
    tipo: Mapped[str] = mapped_column(String(20), default="geral")
    assunto: Mapped[str] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(10), default="aberto", index=True)  # 'aberto' ou 'fechado'
    criado: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)


def descrever_erro_db(e) -> str:
    """Diz em português o que provavelmente está mal, sem mostrar o texto do erro (pode conter o endereço da base)."""
    msg = str(e).lower()
    if isinstance(e, ModuleNotFoundError) or "no module named" in msg:
        return f"falta a biblioteca '{getattr(e, 'name', None) or 'desconhecida'}' no requirements.txt (precisa de pg8000)"
    if type(e).__name__ == "ArgumentError" or "could not parse" in msg:
        return "o DATABASE_URL está mal escrito (tem de começar por postgresql://)"
    if "password authentication failed" in msg:
        return "o utilizador ou a palavra-passe do Neon estão errados"
    if "could not translate host name" in msg or "name or service not known" in msg:
        return "o endereço (host) do Neon está errado"
    if "does not exist" in msg and "database" in msg:
        return "o nome da base de dados no endereço não existe"
    if "ssl" in msg:
        return "o Neon exige ligação segura: o endereço deve terminar em ?sslmode=require"
    if "timeout" in msg or "timed out" in msg:
        return "o Neon demorou demasiado a responder (pode estar a acordar: espere um minuto)"
    return f"erro {type(e).__name__} (veja o log do Render)"


def migrar():
    """Acrescenta colunas novas a bases de dados de versões antigas, para evitar 'no such column'.
    Nunca bloqueia o arranque: se algo falhar, só regista no log."""
    try:
        insp = inspect(engine)
        for tabela in Base.metadata.sorted_tables:
            if not insp.has_table(tabela.name):
                continue
            existentes = {c["name"] for c in insp.get_columns(tabela.name)}
            for col in tabela.columns:
                if col.name in existentes:
                    continue
                tipo = col.type.compile(dialect=engine.dialect)
                try:
                    with engine.begin() as con:
                        con.execute(text(f'ALTER TABLE "{tabela.name}" ADD COLUMN "{col.name}" {tipo}'))
                    log.warning("Migração: coluna %s.%s acrescentada", tabela.name, col.name)
                except Exception:
                    log.exception("Migração: não foi possível acrescentar %s.%s", tabela.name, col.name)
        # Conversas antigas não tinham phone_number_id: copia o número da empresa
        with engine.begin() as con:
            con.execute(text(
                "UPDATE conversas SET phone_number_id = (SELECT wa_phone_number_id FROM empresas "
                "WHERE empresas.id = conversas.empresa_id) WHERE phone_number_id IS NULL"))
    except Exception:
        log.exception("Migração automática falhou (o servidor continua a arrancar)")


def init_db():
    """Cria as tabelas que faltam e atualiza as antigas."""
    Base.metadata.create_all(engine)
    migrar()
