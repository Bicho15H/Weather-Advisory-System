import json
from kafka import KafkaConsumer, KafkaProducer
from settings import *
from utils import chunk_text
import time

consumer = KafkaConsumer(
    TOPIC_RAW_ALERTS,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def main():
    print("Chunker consumer started...")

    for message in consumer:
        raw = message.value
        alert_text = raw.get("weather_overview")

        chunks = chunk_text(alert_text)

        for chunk in chunks:
            payload = {
                "chunk_text": chunk,
                "timestamp": int(time.time()),
                "lat": raw.get("lat"),
                "lon": raw.get("lon")
            }
            producer.send(TOPIC_CHUNKS, payload)
            print(f"Chunk sent → {chunk[:50]}...")

if __name__ == "__main__":
    main()
