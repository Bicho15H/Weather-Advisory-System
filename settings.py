import os
from dotenv import load_dotenv

load_dotenv()

# Kafka
KAFKA_BROKER = "127.0.0.1:9092"
TOPIC_RAW_ALERTS = "weather.alerts.raw"
TOPIC_CHUNKS = "weather.alerts.chunks"
TOPIC_EMBEDDINGS = "weather.alerts.embeddings"

# Weather API
WEATHER_API_URL = "https://api.openweathermap.org/data/3.0/onecall/overview?lat=48.8566&lon=2.3522&units=metric"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Vector DB
CHROMADB_COLLECTION = "weather_realtime"
CHROMADB_DIR = "./chroma_db"

# LLM API
LLM_URL = "https://router.huggingface.co/v1/chat/completions"
LLM_API_KEY = os.getenv("LLM_API_KEY")
