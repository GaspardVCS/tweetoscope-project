from kafka import KafkaConsumer, KafkaProducer
import json
import pickle
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("broker_list", help="list of brokers")
args = parser.parse_args()

# Initialize the Kafka consumer for the sample topic
consumer = KafkaConsumer("sample",                       
  bootstrap_servers = args.broker_list,
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

# Initialize a kafka porducer
producer = KafkaProducer(
  bootstrap_servers = args.broker_list,
  value_serializer=lambda v: pickle.dumps(v), # change json to pickle
  key_serializer=str.encode
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
    from learner import Learner
    main()