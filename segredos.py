"""Cifra segredos sensíveis guardados na base de dados.

A ENCRYPTION_KEY é convertida numa chave Fernet determinística por hash SHA-256.
Durante uma migração, valores antigos sem o prefixo ``enc:`` continuam legíveis.
"""
import base64
import hashlib
import logging
import os

log = logging.getLogger("mactech.segredos")
_PREFIXO = "enc:"
_fernet = None
_chave_cache = None
_cryptography_indisponivel = False
_avisou = False


def _f():
    """Obtém o cifrador sem deixar falhas de importação derrubarem o servidor."""
    global _fernet, _chave_cache, _cryptography_indisponivel
    chave = os.getenv("ENCRYPTION_KEY", "").strip()
    if not chave:
        return None
    if _cryptography_indisponivel:
        return None
    if _fernet is not None and _chave_cache == chave:
        return _fernet
    try:
        from cryptography.fernet import Fernet
    except (ImportError, ModuleNotFoundError):
        _cryptography_indisponivel = True
        log.error("A biblioteca 'cryptography' não está disponível; cifragem indisponível.")
        return None
    try:
        chave_fernet = base64.urlsafe_b64encode(hashlib.sha256(chave.encode("utf-8")).digest())
        _fernet = Fernet(chave_fernet)
        _chave_cache = chave
        return _fernet
    except Exception:
        log.exception("Não foi possível inicializar a cifragem")
        _fernet = None
        _chave_cache = None
        return None


def cifragem_disponivel() -> bool:
    """Indica se existe chave e a biblioteca Fernet pode ser inicializada."""
    return _f() is not None


def cifrar(valor):
    global _avisou
    if valor is None or valor == "":
        return valor
    valor = str(valor)
    if valor.startswith(_PREFIXO):
        return valor
    f = _f()
    if f is None:
        if not _avisou:
            if os.getenv("ENCRYPTION_KEY", "").strip():
                log.error("ENCRYPTION_KEY existe, mas a cifragem não pôde ser inicializada")
            else:
                log.warning("ENCRYPTION_KEY não definida: segredos serão guardados em texto simples")
            _avisou = True
        return valor
    try:
        return _PREFIXO + f.encrypt(valor.encode("utf-8")).decode("ascii")
    except Exception:
        log.exception("Não foi possível cifrar um segredo")
        return valor


def decifrar(valor):
    if valor is None or valor == "":
        return ""
    valor = str(valor)
    if not valor.startswith(_PREFIXO):
        return valor
    f = _f()
    if f is None:
        log.error("Há segredos cifrados mas a ENCRYPTION_KEY/cifragem não está disponível")
        return ""
    try:
        return f.decrypt(valor[len(_PREFIXO):].encode("ascii")).decode("utf-8")
    except Exception:
        log.error("Não foi possível decifrar um segredo (ENCRYPTION_KEY mudou ou valor corrompido?)")
        return ""
