import json
import time
import requests
from kafka import KafkaProducer
from settings import *

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_weather():
    """Fetches alerts from OpenWeather One Call API."""
    url = f"{WEATHER_API_URL}&appid={WEATHER_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return data
    except Exception as e:
        print("Error fetching weather:", e)
        return None

def main():
    print("Starting Weather API Producer...")
    while True:
        data = fetch_weather()
        if data:
            producer.send(TOPIC_RAW_ALERTS, data)
            print("Pushed weather alert event.")
        time.sleep(30)

if __name__ == "__main__":
    main()
