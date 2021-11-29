from sklearn.ensemble import RandomForestRegressor
import pickle
from kafka import KafkaProducer
import json

producer = KafkaProducer(
  bootstrap_servers = "localhost:9092",                     # List of brokers passed from the command line
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),        # How to serialize the value to a binary buffer
  key_serializer=str.encode                                        # How to serialize the key
)

class Learner:
    def __init__(self, key) -> None:
        self.key = key
        self.X = []
        self.y = []
        self.number_of_sample_to_train = 3
        self.max_sample_cache = 1000
        self.model = RandomForestRegressor(max_depth=2, random_state=0)
    
    def ready_to_train(self):
        return (len(self.X) + 1) % self.number_of_sample_to_train == 0
    
    def process_sample(self, sample):
        print(f"sample {len(self.X)} is being processed...")
        self.X.append(sample["X"])
        self.y.append(sample["W"])
        if self.ready_to_train():
            print("Model is training...")
            print(self.X)
            print(self.y)
            self.model.fit(self.X, self.y)
            self.send_model()

    def send_model(self):
        model = pickle.dump(self.model, open(f"random_forest_{self.key}.pickle", 'wb'))
        print(model)


