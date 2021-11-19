from tweet import Tweet

class Cascade:
    def __init__(self, tweet):
        self.identifier = tweet.cascade
        self.first_message = tweet.msg
        self.rt_mag_time = list() # list of (magnitude, time) of retweet
    
    def process_tweet(self, tweet):
        print(f"Tweet {tweet.id} processed!")
