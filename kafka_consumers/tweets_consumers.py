from kafka import KafkaConsumer, KafkaProducer
import json
from params import params

consumer = KafkaConsumer('tweets',                             # Topic name
  bootstrap_servers = params["brokers"],                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

for msg in consumer:
    print(msg.key, msg.value)