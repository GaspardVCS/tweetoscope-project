from kafka import KafkaConsumer, KafkaProducer
import json
from params import params
from learner import Learner

# Initialize the Kafka consumer for the sample topic
consumer = KafkaConsumer("sample",                       
  bootstrap_servers = params["brokers"],
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

def main():
    # Map where the key is the time window and the value a learner object  
    learner_map = dict()
    for msg in consumer:
        if msg.key not in learner_map:
            learner_map[msg.key] = Learner(msg.key)
        if msg.value["type"] == "sample":
            learner_map[msg.key].process_sample(msg.value)


if __name__ =="__main__":
    main()