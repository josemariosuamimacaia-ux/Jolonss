"""Funções do WhatsApp: validar assinatura da Meta e enviar mensagens."""
import hashlib
import hmac
import time

import requests

from config import cfg


RETENTAR = (429, 500, 502, 503, 504)


def assinatura_valida(corpo: bytes, cabecalho: str | None) -> bool:
    """Confirma HMAC SHA-256 da Meta. Cabeçalho vazio ou mal formado = inválido."""
    if not isinstance(corpo, (bytes, bytearray)) or not cfg.app_secret or not cabecalho:
        return False
    cabecalho = cabecalho.strip()
    if not cabecalho.lower().startswith("sha256="):
        return False
    recebido = cabecalho.split("=", 1)[1].strip()
    if len(recebido) != 64:
        return False
    try:
        int(recebido, 16)
    except ValueError:
        return False
    esperado = hmac.new(cfg.app_secret.encode("utf-8"), bytes(corpo), hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, recebido)


def enviar_texto(token: str, phone_number_id: str, numero: str, texto: str) -> None:
    """Envia uma mensagem de texto com retries apenas para falhas transitórias."""
    if not token or not phone_number_id or not numero:
        raise ValueError("token, phone_number_id e número são obrigatórios")
    texto = str(texto or "").strip()
    if not texto:
        raise ValueError("texto vazio")
    ultimo = None
    for tentativa in range(3):
        r = None
        try:
            r = requests.post(
                f"https://graph.facebook.com/{cfg.graph_version}/{phone_number_id}/messages",
                headers={"Authorization": f"Bearer {token}"},
                json={"messaging_product": "whatsapp", "to": numero,
                      "type": "text", "text": {"body": texto[:4000]}},
                timeout=(10, 30),
            )
            if 200 <= r.status_code < 300:
                return
            ultimo = requests.HTTPError(f"Meta respondeu {r.status_code}: {r.text[:300]}")
            if r.status_code not in RETENTAR:
                raise ultimo
            espera = r.headers.get("Retry-After")
            try:
                atraso = min(10.0, max(0.5, float(espera))) if espera else 1.5 * (tentativa + 1)
            except (TypeError, ValueError):
                atraso = 1.5 * (tentativa + 1)
        except (requests.Timeout, requests.ConnectionError) as exc:
            ultimo = exc
            atraso = 1.5 * (tentativa + 1)
        finally:
            if r is not None:
                r.close()
        if tentativa < 2:
            time.sleep(atraso)
    raise ultimo or RuntimeError("Não foi possível enviar a mensagem ao WhatsApp")
