
class Tweet:
    def __init__(self, kafka_msg=None) -> None:
        """
        If a kafka message is given at the initialisation of the 
        Tweet object, it is initialised with the information in 
        the kafka message
        """
        self.type = ""
        self.msg  = ""
        self.time = 0
        self.magnitude = 0
        self.source = None
        self.info = ""
        self.cascade = None
        self.id = None
        if kafka_msg is not None:
            self.create_tweet(kafka_msg)

    def create_tweet(self, kafka_msg) -> None:
        """
        Update the information of the Tweet object based on the message 
        of a kafka producer.
        Note: In Python, the kafka msg.value is already a dictionnary,
        no need to create a difficult string eater.
        """
        self.type = kafka_msg.value.get("type")
        self.msg = kafka_msg.value.get("msg")
        self.time = kafka_msg.value.get("t")
        self.magnitude = kafka_msg.value.get("m")
        self.source = kafka_msg.key
        self.info = kafka_msg.value.get("info")
        self.cascade = int(self.info.split("=")[1])
        self.id = kafka_msg.value.get("tweet_id")
    
    def create_tweet_dict(self) -> dict:
        """
        Create a pyton dictionnary with the Tweet information, only useful
        for the display function. Might merge both functions.
        """
        tweet_dict = dict()
        tweet_dict["type"] = self.type
        tweet_dict["msg"] = self.msg
        tweet_dict["time"] = self.time
        tweet_dict["maginitude"] = self.magnitude
        tweet_dict["source"] = self.source
        tweet_dict["info"] = self.info
        return tweet_dict
    
    def display(self) -> None:
        """
        Print the tweet information in the form of a dictionnary
        """
        print(self.create_tweet_dict())

