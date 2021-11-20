from estimator import Estimator
from kafka import KafkaConsumer, KafkaProducer
import numpy as np
import json

consumer = KafkaConsumer('cascade_series',                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

producer = KafkaProducer(
  bootstrap_servers = 'localhost:9092',                     # List of brokers passed from the command line
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),        # How to serialize the value to a binary buffer
  key_serializer=str.encode                                        # How to serialize the key
)

def main_estimator():
    estimator = Estimator()
    while True:
        cascade_series = consumer.poll(timeout_ms=100)
        if cascade_series:
            cascade_series = cascade_series.get(list(cascade_series.keys())[0])
        for cascade_serie in cascade_series:
            history = np.array(cascade_serie.value["partial_cascade"])
            observation = int(cascade_serie.value["observation_window"])

            _, params = estimator.compute_MLE(history, observation)
            prediction = int(estimator.prediction(params, history, observation))

            msg = {
                "type": "parameters",
                "cid": cascade_serie.key,
                "msg": None,
                "n_obs": len(history),
                "n_supp": prediction,
                "params": list(params),
            }

            producer.send("cascade_properties", key=str(observation), value=msg) # Send a new message to topic
            producer.flush() # not sure if necessary or not

if __name__ == "__main__":
    main_estimator()
    
    


