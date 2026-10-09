"""Funções do WhatsApp: validar a assinatura da Meta, enviar mensagens (texto e lista) e descarregar áudios/imagens."""
import hashlib
import hmac
import time

import requests

from config import cfg

MAX_MIDIA = 10 * 1024 * 1024   # não descarrega ficheiros com mais de 10 MB


def assinatura_valida(corpo: bytes, cabecalho: str | None) -> bool:
    """Confirma que o pedido veio da Meta (HMAC SHA-256). Cabeçalho vazio ou mal formado = inválido."""
    if not cfg.app_secret or not cabecalho or not cabecalho.startswith("sha256="):
        return False
    esperado = "sha256=" + hmac.new(cfg.app_secret.encode(), corpo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado.encode(), cabecalho.strip().encode())


def _enviar(token: str, phone_number_id: str, corpo: dict) -> None:
    """Envia uma mensagem à Meta. Tenta até 3 vezes em erros temporários (429/5xx/ligação). Lança excepção se falhar."""
    ultimo = None
    for tentativa in range(3):
        try:
            r = requests.post(
                f"https://graph.facebook.com/{cfg.graph_version}/{phone_number_id}/messages",
                headers={"Authorization": f"Bearer {token}"},
                json=corpo,
                timeout=30,
            )
            if r.status_code < 400:
                return
            if r.status_code not in (429, 500, 502, 503, 504):
                r.raise_for_status()   # erro definitivo (token errado, número inválido): não vale repetir
            ultimo = requests.HTTPError(f"Meta respondeu {r.status_code}: {r.text[:200]}")
        except (requests.Timeout, requests.ConnectionError) as e:
            ultimo = e
        if tentativa < 2:
            time.sleep(1.5 * (tentativa + 1))
    raise ultimo


def enviar_texto(token: str, phone_number_id: str, numero: str, texto: str) -> None:
    """Envia texto ao cliente. Lança excepção se falhar."""
    _enviar(token, phone_number_id, {"messaging_product": "whatsapp", "to": numero,
                                     "type": "text", "text": {"body": texto[:4000]}})


def enviar_lista(token: str, phone_number_id: str, numero: str, corpo: str, itens: list, botao: str = "Escolher") -> None:
    """Envia uma lista para tocar (máximo 10 opções). itens = [(id, título)]. Quem chama deve ter um plano B em texto,
    porque a Meta recusa listas mal formadas."""
    if not 1 <= len(itens) <= 10:
        raise ValueError("a lista tem de ter entre 1 e 10 opções")
    linhas = [{"id": str(i)[:200], "title": str(t)[:24]} for i, t in itens]
    _enviar(token, phone_number_id, {
        "messaging_product": "whatsapp", "to": numero, "type": "interactive",
        "interactive": {"type": "list", "body": {"text": corpo[:1000]},
                        "action": {"button": botao[:20], "sections": [{"title": "Opções", "rows": linhas}]}}})


def baixar_midia(token: str, media_id: str) -> tuple:
    """Descarrega um áudio ou imagem recebido. Devolve (bytes, mime_type). Lança excepção se falhar ou for grande."""
    cab = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"https://graph.facebook.com/{cfg.graph_version}/{media_id}", headers=cab, timeout=20)
    r.raise_for_status()
    info = r.json()
    url = info.get("url") or ""
    if not url.startswith("https://"):
        raise ValueError("a Meta não devolveu um endereço válido para o ficheiro")
    if int(info.get("file_size") or 0) > MAX_MIDIA:
        raise ValueError("ficheiro demasiado grande")
    f = requests.get(url, headers=cab, timeout=30, stream=True)
    try:
        f.raise_for_status()
        dados = bytearray()
        for bloco in f.iter_content(65536):
            dados += bloco
            if len(dados) > MAX_MIDIA:
                raise ValueError("ficheiro demasiado grande")
    finally:
        f.close()
    return bytes(dados), info.get("mime_type") or f.headers.get("Content-Type", "")
