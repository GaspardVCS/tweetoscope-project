import argparse
import json
import time
from kafka import KafkaConsumer
from processor import Processor
from tweet import Tweet
from tweetoscopeCollectorParams import TweetoscopeCollectorParams

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("param_file_path", help="Path to the collector parameters file")
args = parser.parse_args()

collector = TweetoscopeCollectorParams(args.param_file_path)

consumer = KafkaConsumer('tweets',                   # Topic name
  bootstrap_servers = collector.kafka.brokers,                        # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

if __name__ == "__main__":
    processor_map = dict()
    for msg in consumer:
        print(msg.key, msg.value)
        tweet = Tweet(msg)
        if tweet.source not in processor_map:
            processor_map[tweet.source] = Processor(tweet.source)
            print(f"New Processor {tweet.source} !!")
        processor_map[tweet.source].process_tweet(tweet)