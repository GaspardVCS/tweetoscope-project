from tweet import Tweet
from cascade import Cascade

class Processor:
    def __init__(self, source:str, params:dict) -> None:
        self.source = source
        self.params = params
        self.cascade_queue = list()
    
    def process_tweet(self, tweet:Tweet) -> None:
        tweet_processed = False
        # Traverse the queue in reverse
        for (t, c) in self.cascade_queue:
            if tweet.cascade == c.identifier:
                c.process_tweet(tweet)
                tweet_processed = True
                self.cascade_queue.remove((t, c))
                self.cascade_queue.append((tweet.time, c))
                break
            # Delete cascade if the last tweet in the cascade is too old
            if c.is_terminated(tweet):
                print(f"Cascade {c.identifier} has been deleted with length {len(c.rt_mag_time)}")
                self.cascade_queue.remove((t, c))
                del c
        if not tweet_processed and tweet.type == "tweet":
            self.cascade_queue.append((tweet.time, Cascade(tweet, self.params)))
            print(f"Cascade {tweet.cascade} added to Processor {self.source}")
