from sklearn.ensemble import RandomForestRegressor
import pickle
from kafka import KafkaProducer
import json
from params import params

producer = KafkaProducer(
  bootstrap_servers = params["brokers"],
  value_serializer=lambda v: pickle.dumps(v), # change json to pickle
  key_serializer=str.encode
)

class Learner:
    def __init__(self, key) -> None:
        self.key = key
        self.X = []
        self.y = []
        self.number_of_sample_to_train = 50
        self.max_sample_cache = 1000
        self.model = RandomForestRegressor(max_depth=20, random_state=0)
    
    def ready_to_train(self):
        return (len(self.X) + 1) % self.number_of_sample_to_train == 0
    
    def process_sample(self, sample):
        self.X.append(sample["X"][1:])
        self.y.append(sample["W"])
        if self.ready_to_train():
            print(f"{self.key} Model is training...")
            self.model.fit(self.X, self.y)
            print("model finished training")
            self.send_model()
            print("model sent!")
            if len(self.X) > self.max_sample_cache:
                self.X = self.X[self.number_of_sample_to_train:]

    def send_model(self):
        producer.send("model", key=self.key, value=self.model)
        


