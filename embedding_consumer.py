import json
from kafka import KafkaConsumer, KafkaProducer
from sentence_transformers import SentenceTransformer
from settings import *

model = SentenceTransformer("all-MiniLM-L6-v2")

consumer = KafkaConsumer(
    TOPIC_CHUNKS,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest"
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def main():
    print("Embedding consumer running...")

    for msg in consumer:

        chunk_data = msg.value
        text = chunk_data["chunk_text"]
        embedding = model.encode(text).tolist()

        out = {
            "text": text,
            "embedding": embedding,
            "timestamp": chunk_data["timestamp"],
            "lat": chunk_data["lat"],
            "lon": chunk_data["lon"]
        }

        producer.send(TOPIC_EMBEDDINGS, out)
        print("Generated embedding →", text[:50])

if __name__ == "__main__":
    main()
