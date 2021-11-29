from kafka import KafkaConsumer, KafkaProducer
import json
from learner import Learner

consumer = KafkaConsumer("sample",                       
  bootstrap_servers = "localhost:9092",
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

if __name__ =="__main__":
    learner_map = dict()
    for msg in consumer:
        if msg.key not in learner_map:
            learner_map[msg.key] = Learner(msg.key)
        if msg.value["type"] == "sample":
            learner_map[msg.key].process_sample(msg.value)
