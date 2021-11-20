from kafka import KafkaProducer

class Predictor:
    def __init__(self, params):
        self.key = params["key"]
        self.producer = KafkaProducer()
    
    def process_message(self, message):
        if message["type"] == "size":
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

            # TODO: send message with stat to the stat topic

        elif message["type"] == "parameters":
            # TODO: update map to create the samples that will be send to the sample topic
            pass
        else:
            print("ERROR") # add true error

    def predict(self, message):
        prediction = message["n_prob"]
        return prediction