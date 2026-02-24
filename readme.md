# MoreApp → Webhook → Pub/Sub → BigQuery (RAW)

## Servicios
- Webhook: `/webhook/moreapp` (valida firma MoreApp + publica en Pub/Sub)
- Worker: `/pubsub/push` (consume Pub/Sub push + inserta en BigQuery)

## Local
```bash
cp .env.example .env
export $(cat .env | xargs)
docker build -t moreapp .
docker run -p 8080:8080 --env-file .env moreapp
