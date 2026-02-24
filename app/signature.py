import hmac
import hashlib
import time

def parse_signature_header(header_value: str) -> tuple[str, int, str]:
    # Acepta: "t=..., v1=..." o "t=...,v1=..."
    parts = [p.strip() for p in header_value.split(",")]
    kv = {}
    for p in parts:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        kv[k.strip()] = v.strip()

    if "t" not in kv or "v1" not in kv:
        raise ValueError("Missing t or v1 in signature header")

    t_raw = kv["t"]              # 👈 STRING EXACTA como viene en el header
    v1 = kv["v1"]

    t_int = int(t_raw)           # 👈 para tolerancia
    t_seconds = t_int // 1000 if t_int > 10**12 else t_int

    return t_raw, t_seconds, v1

def verify_moreapp_signature(signature_header: str, raw_body: bytes, secret: str, tolerance_seconds: int = 300) -> None:
    t_raw, t_seconds, received_sig = parse_signature_header(signature_header)

    now = int(time.time())
    if abs(now - t_seconds) > tolerance_seconds:
        raise ValueError("Timestamp outside tolerance")

    # 👇 IMPORTANTE: firmar con t_raw tal cual, NO con segundos normalizados
    signed_payload = t_raw.encode("utf-8") + b"." + raw_body

    expected_sig = hmac.new(
        key=secret.encode("utf-8"),
        msg=signed_payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, received_sig):
        raise ValueError("Invalid signature")
