import json
from uuid import uuid4
from kafka import KafkaConsumer
import chromadb
from chromadb.utils import embedding_functions
from settings import *

# Initialize Chroma client
client = chromadb.PersistentClient(path=CHROMADB_DIR)

# Create or get the collection
collection = client.get_or_create_collection(
    name=CHROMADB_COLLECTION,
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

consumer = KafkaConsumer(
    TOPIC_EMBEDDINGS,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest"
)

def main():
    print("Indexer running...")

    for msg in consumer:
        data = msg.value

        # Upsert the embedding and its associated metadata to Chroma
        collection.add(
            documents=[data["text"]],
            metadatas=[{
                "timestamp": data["timestamp"],
                "lat": data["lat"],
                "lon": data["lon"]
            }],
            ids=[str(uuid4())],
            embeddings=[data["embedding"]]  # Embedding vector
        )
        print("Indexed chunk:", data["text"][:50])

if __name__ == "__main__":
    main()
