import os

class Settings:
    # MoreApp webhook secret (para validar MoreApp-Signature)
    MOREAPP_WEBHOOK_SECRET: str = os.getenv("MOREAPP_WEBHOOK_SECRET", "")

    # GCP
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    PUBSUB_TOPIC_ID: str = os.getenv("PUBSUB_TOPIC_ID", "moreapp-events")

    # BigQuery destino RAW
    BQ_DATASET: str = os.getenv("BQ_DATASET", "granier_raw")
    BQ_TABLE: str = os.getenv("BQ_TABLE", "moreapp_submissions_raw")

    # Seguridad anti-replay
    SIGNATURE_TOLERANCE_SECONDS: int = int(os.getenv("SIGNATURE_TOLERANCE_SECONDS", "300"))

settings = Settings()
