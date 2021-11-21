from copy import Error
import json
from kafka import KafkaProducer

class Predictor:
    def __init__(self, params):
        self.key = params["key"]
        self.producer = KafkaProducer(bootstrap_servers = params["brokers"],
                                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                    key_serializer=str.encode)
        self.cascade_map = dict()
    
    def process_message(self, message):
        self.update_map(message)
        cid = message["cid"]
        if (message["type"] == "size") and cid in self.cascade_map:
            # Send message to the sample topic for training
            sample_key = self.key
            sample_message = {
                "type": "sample",
                "cid": cid,
                "X": self.cascade_map[cid]["params"], # p, beta, n_star, G1
                "W": self.cascade_map[cid]["W"]
            }

            self.producer.send("sample", key=sample_key, value=sample_message) # Send a new message to topic
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

            self.producer.send("stat", key=stat_key, value=stat_message) # Send a new message to topic
            self.producer.flush() # not sure if necessary or not

            del self.cascade_map[cid]
            
        elif message["type"] == "parameters":
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
            self.producer.send("alert", key=alert_key, value=alert_message) # Send a new message to topic
            self.producer.flush() # not sure if necessary or not


    def predict(self, message):
        prediction = message["n_supp"]
        return prediction

    def update_map(self, message):
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

    @staticmethod
    def find_true_omega(cascade_dict):
        _, _, n_star, G1 = cascade_dict["params"]
        W = cascade_dict["n_tot"] - cascade_dict["n_obs"]
        W *= (1 - n_star) / G1
        return W 

    @staticmethod
    def compute_are(n_pred, n_true):
        return abs(n_true - n_pred) / n_true