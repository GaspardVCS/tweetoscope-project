from kafka import KafkaProducer

class Predictor:
    def __init__(self, params):
        self.key = params["key"]
        self.producer = KafkaProducer()
        self.cascade_map = dict()
    
    def process_message(self, message):
        if message["type"] == "size":
            self.update_map(message)
            prediction = self.predict(message)

            alert_key = ""
            alert_message = {
                "type": "alert",
                "cid": message["cid"],
                "msg": None,
                "T_obs": self.key,
                "n_tot": prediction,
            }
            self.producer.send("alert", key=alert_key, value=alert_message) # Send a new message to topic
            self.producer.flush() # not sure if necessary or not

            # TODO: update map to send samples to sample topic
            sample_key = self.key
            cid = message["cid"]
            sample_message = {
                "type": "sample",
                "cid": cid,
                "X": self.cascade_map[cid]["params"], # p, beta, n_star, G1
                "W": self.cascade_map[cid]["W"]
            }

            # TODO: send message with stat to the stat topic

        elif message["type"] == "parameters":
            # TODO: update map to create the samples that will be send to the sample topic
            pass
        else:
            print("ERROR") # add true error

    def predict(self, message):
        prediction = message["n_prob"]
        return prediction

    def update_map(self, message):
        cid = message["cid"]
        if message["type"] == "params":
            self.cascade_map[cid] = {
                "params": message["params"],
                "cascade_serie": message["tweets"],
            }
        elif message["type"] == "size":
            if cid in self.cascade_map:
                self.map[cid]["n_tot"] = message["n_tot"]
                W = self.find_true_omega(self.cascade_map[cid])
                self.map[cid]["W"] = W
    
    def find_true_omega(self, cascade_dict):
        _, _, n_star, G1 = cascade_dict["params"]
        W = cascade_dict["n_tot"] - len(cascade_dict["cascade_serie"])
        W *= (1 - n_star) / G1
        return W 
