from tweet import Tweet
import time
from cascade import Cascade

class Processor:
    def __init__(self, source, params):
        self.source = source
        self.params = params
        self.cascade_queue = list() # see queue in python, list for now
        #TODO: change list to queue
    
    def process_tweet(self, tweet):
        tweet_processed = False
        for c in self.cascade_queue:
            #TODO: add deletion of cascade if timestamp
            if tweet.cascade == c.identifier:
                c.process_tweet(tweet)
                tweet_processed = True
                break
            # Delete cascade if it is too old
            if c.is_terminated(tweet):
                print(f"Cascade {c.identifier} has been deleted")
                self.cascade_queue.remove(c)
                del c


        if not tweet_processed and tweet.type == "tweet":
            self.cascade_queue.append(Cascade(tweet, self.params["terminated"]))
            print(f"Cascade {tweet.cascade} added to Processor {self.source}")

