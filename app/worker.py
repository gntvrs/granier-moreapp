import base64
import json
from fastapi import FastAPI, Request, HTTPException
from app.settings import settings
from app.bq_client import insert_raw_event
import logging

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/pubsub/push")
async def pubsub_push(request: Request):
    body = await request.json()

    # Formato estándar Push Pub/Sub:
    # { "message": { "data": "base64...", "messageId": "...", ... }, "subscription": "..." }
    if "message" not in body or "data" not in body["message"]:
        raise HTTPException(status_code=400, detail="Invalid Pub/Sub message")

    data_b64 = body["message"]["data"]
    raw = base64.b64decode(data_b64).decode("utf-8")

    try:
        event = json.loads(raw)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON in Pub/Sub data")

    try:
        insert_raw_event(settings.GCP_PROJECT_ID, settings.BQ_DATASET, settings.BQ_TABLE, event)
    except Exception as e:
        logging.exception("BQ insert failed")  # imprime stacktrace en stderr
        raise HTTPException(status_code=500, detail=f"BQ insert failed: {str(e)}")

    return {"status": "ok"}
