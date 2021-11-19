import argparse
import json
import time
from kafka import KafkaConsumer, KafkaProducer
from tweetoscopeCollectorParams import TweetoscopeCollectorParams

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("param_file_path", help="Path to the collector parameters file")
args = parser.parse_args()

collector = TweetoscopeCollectorParams(args.param_file_path)
params = {
  "terminated": collector.times.terminated,
  "observations": collector.times.observations,
  "min_cascade_size": collector.cascade.min_cascade_size,
}
consumer = KafkaConsumer('tweets',                             # Topic name
  bootstrap_servers = collector.kafka.brokers,                 # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

producer = KafkaProducer(
  bootstrap_servers = collector.kafka.brokers,                     # List of brokers passed from the command line
  value_serializer=lambda v: json.dumps(v).encode('utf-8'),        # How to serialize the value to a binary buffer
  key_serializer=str.encode                                        # How to serialize the key
)

if __name__ == "__main__":
    from processor import Processor
    from tweet import Tweet
    processor_map = dict()
    for msg in consumer:
        tweet = Tweet(msg)
        if tweet.source not in processor_map:
            processor_map[tweet.source] = Processor(tweet.source, params)
            print(f"New Processor {tweet.source} !!")
        processor_map[tweet.source].process_tweet(tweet)
        del tweet