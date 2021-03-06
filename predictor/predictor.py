from copy import Error
import json
from kafka import KafkaProducer

class Predictor:
    def __init__(self, params:dict) -> None:
        self.key = params["key"]
        self.producer = KafkaProducer(bootstrap_servers = params["brokers"],
                                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                    key_serializer=str.encode)
        self.model = None
        self.cascade_map = dict()
    
    def process_message(self, message:dict) -> None:
        """
        Process the new message. First update the cascade information based on the new message. 
        Then send messages to the different kafka topics if needed.
        """
        self.update_map(message)
        cid = message["cid"]
        if message["type"] == "parameters":
            # Get the prediction
            prediction = self.predict(message)
            self.cascade_map[cid]["prediction"] = prediction
            # Send message to the alert topic
            alert_key = ""
            alert_message = {
                "type": "alert",
                "cid": cid,
                "msg": None,
                "T_obs": self.key,
                "n_tot": prediction,
            }
            self.producer.send("alert", key=alert_key, value=alert_message)
            self.producer.flush() # not sure if necessary or not

        elif (message["type"] == "size") and cid in self.cascade_map:
            # Send message to the sample topic for training
            sample_key = self.key
            sample_message = {
                "type": "sample",
                "cid": cid,
                "X": self.cascade_map[cid]["params"], # p, beta, n_star, G1
                "W": self.cascade_map[cid]["W"]
            }

            self.producer.send("sample", key=sample_key, value=sample_message)
            self.producer.flush() # not sure if necessary or not

            # Send the prediction error to the stat topic
            n_true = self.cascade_map[cid]["n_tot"]
            n_pred = self.cascade_map[cid]["prediction"]
            stat_key = ""
            stat_message = {
                "type": "stat",
                "cid": cid,
                "T_obs": self.key,
                "ARE": self.compute_are(n_pred, n_true),
            }

            self.producer.send("stat", key=stat_key, value=stat_message)
            self.producer.flush() # not sure if necessary or not

            del self.cascade_map[cid]
            
        

    def predict(self, message:dict) -> float:
        """
        Return the prediction. Uses the one of the hawkes estimator if
        no model is available.
        """
        if self.model is not None:
            X = message["params"]
            w = self.model.predict([X])[0]
            n, n_star, G1 = message["n_obs"], X[2], X[3]
            prediction = n + w * G1 / (1 - n_star)
        else:
            prediction = message["n_supp"]
        return prediction

    def update_map(self, message:dict) -> None:
        """
        Update the information of a given cascade. First, we get the parameters given by the 
        Hawkes estimator. Second, we get the real size of the cascade. 
        """
        cid = message["cid"]
        if message["type"] == "parameters":
            self.cascade_map[cid] = {
                "params": message["params"],
                "n_obs": message["n_obs"],
            }
        elif message["type"] == "size":
            if cid in self.cascade_map:
                self.cascade_map[cid]["n_tot"] = message["n_tot"]
                W = self.find_true_omega(self.cascade_map[cid])
                self.cascade_map[cid]["W"] = W
        else:
            raise Error # Not sure about the syntax
    
    def update_model(self, model):
        """
        Replace the old model by the new one
        """
        del self.model
        self.model = model

    @staticmethod
    def find_true_omega(cascade_dict:dict) -> float:
        """
        Calculate the real omega that has to be predicted by the model
        """
        _, _, n_star, G1 = cascade_dict["params"]
        W = cascade_dict["n_tot"] - cascade_dict["n_obs"]
        W *= (1 - n_star) / G1
        return W 

    @staticmethod
    def compute_are(n_pred:float, n_true:int) -> float:
        """
        Calculate the ARE metric
        """
        return abs(n_true - n_pred) / n_true