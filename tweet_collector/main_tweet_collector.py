import argparse
import json
from kafka import KafkaConsumer, KafkaProducer
from tweetoscopeCollectorParams import TweetoscopeCollectorParams

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("param_file_path", help="Path to the collector parameters file")
args = parser.parse_args()

collector = TweetoscopeCollectorParams(args.param_file_path)

# parameters needed for the Processor
params = {
  "brokers": collector.kafka.brokers,
  "in": collector.topic.in_,
  "terminated": collector.times.terminated,
  "observations": collector.times.observations,
  "min_cascade_size": collector.cascade.min_cascade_size,
  "out_series": collector.topic.out_series,
  "out_properties": collector.topic.out_properties,
}

# Initialize Kafka consumer and producer
consumer = KafkaConsumer(params["in"],
  bootstrap_servers = params["brokers"],
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),
  key_deserializer= lambda v: v.decode()
)

producer = KafkaProducer(
  bootstrap_servers = collector.kafka.brokers,
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),
  key_serializer=str.encode
)

def main():
  processor_map = dict()
  print("Initialisation done!")
  for msg in consumer:
    tweet = Tweet(msg)
    if tweet.source not in processor_map:
        processor_map[tweet.source] = Processor(tweet.source, params)
        print(f"New Processor {tweet.source} !!")
    processor_map[tweet.source].process_tweet(tweet)
    del tweet

if __name__ == "__main__":
    from processor import Processor
    from tweet import Tweet

    main()
    