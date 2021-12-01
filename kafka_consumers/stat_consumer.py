from kafka import KafkaConsumer, KafkaProducer
import json
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("broker_list", help="list of brokers")
args = parser.parse_args()

consumer = KafkaConsumer('stat',
  bootstrap_servers = args.broker_list,
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

for msg in consumer:
    print(msg.key, msg.value)