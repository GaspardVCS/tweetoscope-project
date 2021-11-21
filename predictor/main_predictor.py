import json
from kafka import KafkaConsumer, KafkaProducer
from predictor import Predictor

consumer = KafkaConsumer('cascade_properties',                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

if __name__ == "__main__":
    predictor_map = dict()
    for msg in consumer:
        if msg.key not in predictor_map:
            params = {
                "key": msg.key,
                "brokers": "localhost:9092",
            }
            predictor_map[msg.key] = Predictor(params)
        predictor_map[msg.key].process_message(msg.value)
