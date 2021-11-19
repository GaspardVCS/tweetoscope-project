from tweet import Tweet

class Cascade:
    def __init__(self, tweet, terminated):
        self.identifier = tweet.cascade
        self.first_message = tweet.msg
        self.rt_mag_time = [(tweet.time, tweet.magnitude)] # list of (magnitude, time) of retweet
        self.terminated = int(terminated)

    def process_tweet(self, tweet):
        """
        Add the retweet time and retweet maginitude 
        to the cascade
        """
        self.rt_mag_time.append((tweet.time, tweet.magnitude))
        print(f"Tweet {tweet.id} processed at time {tweet.time}")
    
    def is_terminated(self, tweet):
        """
        Return True if the last tweet in the cascade was seen more than
        terminated seconds before the current tweet. If so the cascade 
        should be deleted. 
        """
        return (tweet.time - self.rt_mag_time[-1][0] > self.terminated)
