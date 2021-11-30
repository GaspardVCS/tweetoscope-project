from estimator import Estimator
from kafka import KafkaConsumer, KafkaProducer
import numpy as np
import json
from params import params

# Initialize Kafka consumer for the cascade_series topic
consumer = KafkaConsumer('cascade_series',                             # Topic name
  bootstrap_servers = params["brokers"],                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

# Initialize Kafka producer
producer = KafkaProducer(
  bootstrap_servers = params["brokers"],                     # List of brokers passed from the command line
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),        # How to serialize the value to a binary buffer
  key_serializer=str.encode                                        # How to serialize the key
)

def main_estimator() -> None:
    estimator = Estimator()
    while True:
        cascade_series = consumer.poll(timeout_ms=100)
        if cascade_series:
            cascade_series = cascade_series.get(list(cascade_series.keys())[0])
        for cascade_serie in cascade_series:
            history = np.array(cascade_serie.value["tweets"])
            observation = int(cascade_serie.value["T_obs"])

            _, params = estimator.compute_MLE(history, observation)
            params = list(params)
            N_tot, n_star, G1 = estimator.prediction(params, history, observation)
            params.append(n_star)
            params.append(G1)

            msg = {
                "type": "parameters",
                "cid": cascade_serie.value["cid"],
                "msg": None,
                "n_obs": len(history),
                "n_supp": N_tot,
                "params": list(params), # p, beta, n_star, G1
            }

            producer.send("cascade_properties", key=str(observation), value=msg)
            producer.flush() # not sure if necessary or not

if __name__ == "__main__":
    main_estimator()
    
    


