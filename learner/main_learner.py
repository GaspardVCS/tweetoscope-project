from kafka import KafkaConsumer, KafkaProducer
import json
from learner import Learner

consumer = KafkaConsumer("sample",                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

if __name__ =="__main__":
    learner_map = dict()
    for msg in consumer:
        if msg.key not in learner_map:
            learner_map[msg.key] = Learner(msg.key)
        if msg.value["type"] == "sample":
            print(msg.key)
            learner_map[msg.key].process_sample(msg.value)
            if len(learner_map[msg.key].X) > 3:
                prediction = learner_map[msg.key].model.predict([msg.value["X"]])
                print("prediction", prediction)
