
class Tweet:
    def __init__(self, kafka_msg = None):
        """
        If a kafka message is given at the initialisation of the 
        Tweet object, it is initialised with the information in 
        the kafka message
        """
        self.type = ""
        self.msg  = ""
        self.time = 0
        self.magnitude = 0
        self.source = 0
        self.info = ""
        if kafka_msg is not None:
            self.create_tweet(kafka_msg)

    def create_tweet(self, kafka_msg):
        """
        Update the information of the Tweet object based on the message 
        of a kafka producer.
        Note: In Python, the kafka msg.value is already a dictionnary,
        no need to create a difficult string eater.
        """
        self.type = kafka_msg.get("type")
        self.msg = kafka_msg.get("msg")
        self.time = kafka_msg.get("t")
        self.magnitude = kafka_msg.get("m")
        self.source = kafka_msg.get("source")
        self.info = kafka_msg.get("info")
    
    def create_tweet_dict(self):
        """
        Create a pyton dictionnary with the Tweet information
        """
        tweet_dict = dict()
        tweet_dict["type"] = self.type
        tweet_dict["msg"] = self.msg
        tweet_dict["time"] = self.time
        tweet_dict["maginitude"] = self.magnitude
        tweet_dict["source"] = self.source
        tweet_dict["info"] = self.info
        return tweet_dict
    
    def display(self):
        """
        Print the tweet information in the form of a dictionnary
        """
        print(self.create_tweet_dict())

