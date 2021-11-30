from kafka import KafkaConsumer, KafkaProducer
import pickle
from params import params

consumer = KafkaConsumer('model',                             # Topic name
  bootstrap_servers = params["brokers"],                 # List of brokers passed from the command line
  value_deserializer=lambda v: pickle.loads(v),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

for msg in consumer:
    print(msg.key, msg.value)
    X = [[1.022, 2.36, 5.24, 0.2225]]
    prediction = msg.value.predict(X)
    print(prediction)