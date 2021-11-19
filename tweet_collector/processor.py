from tweet import Tweet
from cascade import Cascade

class Processor:
    def __init__(self, source):
        self.source = source
        self.cascade_queue = list() # see queue in python, list for now
    
    def process_tweet(self, tweet):
        cascade_identifier = tweet.cascade
        tweet_processed = False
        for c in self.cascade_queue:
            if cascade_identifier == c.identifier:
                c.process_tweet(tweet)
                tweet_processed = True
                break
        if not tweet_processed:
            self.cascade_queue.append(Cascade(tweet))
            print(f"Cascade {tweet.cascade} added to Processor {self.source}")

