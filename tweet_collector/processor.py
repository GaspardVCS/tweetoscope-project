from tweet import Tweet
import time
from cascade import Cascade

class Processor:
    def __init__(self, source, params):
        self.source = source
        self.params = params
        self.cascade_queue = list()
    
    def process_tweet(self, tweet):
        tweet_processed = False
        # Traverse the queue in reverse
        for i, (t, c) in zip(range(len(self.cascade_queue) - 1, -1, -1), self.cascade_queue[::-1]):
            if tweet.cascade == c.identifier:
                c.process_tweet(tweet)
                tweet_processed = True
                new_cascade = self.cascade_queue.pop(i)
                self.cascade_queue.append((tweet.time, new_cascade[1]))
                break
            # Delete cascade if the last tweet in the cascade is too old
            if c.is_terminated(tweet):
                print(f"Cascade {c.identifier} has been deleted")
                self.cascade_queue.remove((t, c))
                del c
        if not tweet_processed and tweet.type == "tweet":
            self.cascade_queue.append((tweet.time, Cascade(tweet, self.params)))
            print(f"Cascade {tweet.cascade} added to Processor {self.source}")
