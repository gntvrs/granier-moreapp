import json
from google.cloud import pubsub_v1

def publish_event(project_id: str, topic_id: str, event: dict) -> str:
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = json.dumps(event, ensure_ascii=False).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    return future.result()  # message_id
