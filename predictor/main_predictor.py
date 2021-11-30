import json
import pickle
from kafka import KafkaConsumer, KafkaProducer
from predictor import Predictor
from params import params

# Initialize two consumers for the topics cascade_properties and model
consumer_properties = KafkaConsumer('cascade_properties',
  bootstrap_servers = params["brokers"],
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

consumer_model = KafkaConsumer('model',
  bootstrap_servers = params["brokers"],
  value_deserializer=lambda v: pickle.loads(v),
  key_deserializer= lambda v: v.decode()
)

def main():
    # Create a map where key is the time window and value a predictor object
    predictor_map = dict()
    while True:
        cascade_properties = consumer_properties.poll(timeout_ms=100)
        if cascade_properties:
            cascade_properties = cascade_properties.get(list(cascade_properties.keys())[0])
            for msg in cascade_properties:
                if msg.key not in predictor_map:
                    params = {
                        "key": msg.key,
                        "brokers": params["brokers"],
                    }
                    predictor_map[msg.key] = Predictor(params)
                predictor_map[msg.key].process_message(msg.value)

        model_msg = consumer_model.poll(timeout_ms=100)
        if model_msg:
            model_msg = model_msg.get(list(model_msg.keys())[0])
            for msg in model_msg:
                # Should not append but just in case
                if msg.key not in predictor_map:
                    pass
                else:
                    predictor_map[msg.key].update_model(msg.value)

if __name__ == "__main__":
    main()

