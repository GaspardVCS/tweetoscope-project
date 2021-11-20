from estimator import Estimator
from kafka import KafkaConsumer
import numpy as np
import json

consumer1 = KafkaConsumer('cascade_series',                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

consumer2 = KafkaConsumer('cascade_properties',                             # Topic name
  bootstrap_servers = "localhost:9092",                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)


if __name__ == "__main__":
    predictor = Estimator()
    results = dict()
    while True:
        cascade_series = consumer1.poll(timeout_ms=100)
        if cascade_series:
            cascade_series = cascade_series.get(list(cascade_series.keys())[0])
        cascade_properties = consumer2.poll(timeout_ms=100)
        if cascade_properties:
            cascade_properties = cascade_properties.get(list(cascade_properties.keys())[0])
        for cascade_serie in cascade_series:
            history = np.array(cascade_serie.value["partial_cascade"])
            observation = int(cascade_serie.value["observation_window"])

            _, params = predictor.compute_MLE(history, observation)
            prediction = predictor.prediction(params, history, observation)

            if int(cascade_serie.key) not in results:
                results[int(cascade_serie.key)] = dict()
            results[int(cascade_serie.key)][observation] = int(prediction)
        for cascade_property in cascade_properties:
            if int(cascade_property.key) in results:
                results[int(cascade_property.key)]["real"] = cascade_property.value["number_retweet"]
                print(cascade_property.key, results[int(cascade_property.key)])
