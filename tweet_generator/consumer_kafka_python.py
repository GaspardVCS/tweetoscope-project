import sys
sys.path.append("..")
import argparse                   # To parse command line arguments
import json
from time import time                       # To parse and dump JSON
from kafka import KafkaConsumer   # Import Kafka consumer
import time
from tweet_collector.tweet import Tweet
 
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--broker-list', type=str, required=True, help="the broker list")
args = parser.parse_args()  # Parse arguments

consumer = KafkaConsumer('tweets',                   # Topic name
  bootstrap_servers = args.broker_list,                        # List of brokers passed from the command line
  value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # How to deserialize the value from a binary buffer
  key_deserializer= lambda v: v.decode()                       # How to deserialize the key (if any)
)

def display_message(msg):
  type_ = msg.value["type"]
  message = msg.value["msg"]
  t = msg.value["t"]
  magnitude = msg.value["m"]
  tweet_id = msg.value["tweet_id"]
  info = msg.value["info"]
  print(f"{msg.key},\
  type: {type_},\
  msg: {message},\
  t: {t},\
  m: {magnitude},\
  tweet_id: {tweet_id},\
  info: {info}")

for msg in consumer:                            # Blocking call waiting for a new message
    print(msg.key, msg.value)
    tweet = Tweet(msg)
    tweet.display()
    time.sleep(5)
    # display_message(msg)                        # Write key and payload of the received message