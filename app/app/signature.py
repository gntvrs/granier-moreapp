import hmac
import hashlib
import time

def parse_signature_header(header_value: str) -> tuple[int, str]:
    # Formato esperado: t=1234567890, v1=abcdef...
    # Ojo: a veces viene sin espacios
    parts = [p.strip() for p in header_value.split(",")]
    kv = {}
    for p in parts:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        kv[k.strip()] = v.strip()
    if "t" not in kv or "v1" not in kv:
        raise ValueError("Missing t or v1 in signature header")
    return int(kv["t"]), kv["v1"]

def verify_moreapp_signature(
    signature_header: str,
    raw_body: bytes,
    secret: str,
    tolerance_seconds: int = 300,
) -> None:
    ts, received_sig = parse_signature_header(signature_header)

    now = int(time.time())
    if abs(now - ts) > tolerance_seconds:
        raise ValueError("Timestamp outside tolerance")

    payload = f"{ts}.{raw_body.decode('utf-8')}"
    expected_sig = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, received_sig):
        raise ValueError("Invalid signature")
