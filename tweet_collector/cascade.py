from tweet import Tweet
from main_tweet_collector import producer
import copy

class Cascade:
    def __init__(self, tweet, params):
        self.identifier = tweet.cascade
        self.starting_time = tweet.time
        self.first_message = tweet.msg
        self.rt_mag_time = [(tweet.time, tweet.magnitude)] # list of (magnitude, time) of retweet
        self.params = params
        self.observations_to_send = copy.deepcopy(params["observations"])

    def process_tweet(self, tweet):
        """
        Add the retweet time and retweet maginitude 
        to the cascade
        """
        self.rt_mag_time.append((tweet.time, tweet.magnitude))
        # print(f"Tweet {tweet.id} processed at time {tweet.time}")
        for o in self.observations_to_send:
            if (tweet.time - self.starting_time) > int(o):
                self.send_partial_cascade(o)
                self.observations_to_send.remove(o) # We don't want to send the same observations multiple times

    def is_terminated(self, tweet):
        """
        Return True if the last tweet in the cascade was seen more than
        terminated seconds before the current tweet. If so the cascade 
        should be deleted. 
        """
        if (tweet.time - self.rt_mag_time[-1][0] > int(self.params["terminated"])) \
            and (len(self.rt_mag_time) >= self.params["min_cascade_size"]):
            # if there are still observations windows that weren't send, we send them
            # NOTE: maybe send them only at the end of the cascade?
            for o in self.observations_to_send: 
                self.send_partial_cascade(o)
            self.send_cascade_properties()
            return True
        return False
    
    def send_partial_cascade(self, observation):
        """
        Send the partial cascade for the observation window to the 
        kafka topic 'cascade_series'
        """
        msg = {
            "type": "serie",
            "cid": self.identifier,
            "msg": None, 
            "T_obs": int(observation),
            "tweets": [[elem[0] - self.starting_time, elem[1]] for elem in self.rt_mag_time \
                                if (elem[0] - self.starting_time) < int(observation)],
        }
        producer.send(self.params["out_series"], key="", value=msg) # Send a new message to topic
        producer.flush() # not sure if necessary or not
    
    def send_cascade_properties(self):
        """
        Send the cascade properties to the kafka topic 'cascade_properties'
        """
        for observation in self.params["observations"]:
            msg = {
                "type": "size",
                "cid": self.identifier,
                "n_tot": len(self.rt_mag_time),
                "t_end": self.rt_mag_time[-1][0],
            }
            producer.send(self.params["out_properties"], key=str(observation), value=msg) # Send a new message to topic
            producer.flush() # not sure if necessary or not
