import json
from fastapi import FastAPI, Request, HTTPException
from app.settings import settings
from app.signature import verify_moreapp_signature
from app.pubsub_client import publish_event

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/webhook/moreapp")
async def moreapp_webhook(request: Request):
    raw_body = await request.body()
    sig = request.headers.get("MoreApp-Signature")

    if not sig:
        raise HTTPException(status_code=400, detail="Missing MoreApp-Signature header")
    if not settings.MOREAPP_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Server not configured (missing secret)")

    try:
        verify_moreapp_signature(
            signature_header=sig,
            raw_body=raw_body,
            secret=settings.MOREAPP_WEBHOOK_SECRET,
            tolerance_seconds=settings.SIGNATURE_TOLERANCE_SECONDS,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Signature verification failed: {str(e)}")

    try:
        event = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    # Publica a Pub/Sub
    try:
        msg_id = publish_event(settings.GCP_PROJECT_ID, settings.PUBSUB_TOPIC_ID, event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pub/Sub publish failed: {str(e)}")

    return {"status": "ok", "message_id": msg_id}
