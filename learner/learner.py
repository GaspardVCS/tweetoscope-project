from sklearn.ensemble import RandomForestRegressor
import pickle
from kafka import KafkaProducer
import json
from params import params

# Initialize a kafka porducer
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
        self.number_of_sample_to_train = 20
        self.max_sample_cache = 1000
        self.model = RandomForestRegressor(max_depth=10, random_state=0)
    
    def ready_to_train(self) -> bool:
        """
        Returns true if number_of_sample_to_train new samples are available
        """
        return (len(self.X) + 1) % self.number_of_sample_to_train == 0
    
    def process_sample(self, sample):
        """
        Add new sample to the training dataset. Train the model if enough samples are available
        """
        self.X.append(sample["X"])
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
        """
        Send the trained model in the topic 'model'
        """
        producer.send("model", key=self.key, value=self.model)
        


