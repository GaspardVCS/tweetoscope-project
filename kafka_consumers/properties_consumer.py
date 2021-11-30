from kafka import KafkaConsumer, KafkaProducer
import json


consumer = KafkaConsumer('cascade_properties',                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

for msg in consumer:
    print(msg.key, msg.value)