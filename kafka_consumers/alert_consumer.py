from kafka import KafkaConsumer, KafkaProducer
import json
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("broker_list", help="list of brokers")
args = parser.parse_args()

consumer = KafkaConsumer('alert',                             # Topic name
  bootstrap_servers = args.broker_list,                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

for msg in consumer:
    print(msg.key, msg.value)