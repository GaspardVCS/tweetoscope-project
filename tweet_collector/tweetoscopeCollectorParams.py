

class Kafka:
    def __init__(self):
        self.brokers = None

class Topic:
    def __init__(self):
        self.in_ = None 
        self.out_series = None  
        self.out_properties = None

class Times:
    def __init__(self):
        self.observations = []
        self.terminated = None

class CascadeParam:
    def __init__(self):
        self.min_cascade_size = None
	

class TweetoscopeCollectorParams:
    def __init__(self, param_file_path):
        self.kafka = Kafka()
        self.topic = Topic()
        self.times = Times()
        self.cascade = CascadeParam()
        self.param_file_path = param_file_path
        self.current_section = None

        self._collector()
    
    def _parse_line(self, line):
        if line.startswith("["):
            self.current_section = line[1:].split("]")[0]
            return
        elif len(line.split("=")) == 2:
            key, value = line.split("=")
            return key, value
    
    def _collector(self):
        with open(self.param_file_path, "r") as f:
            file = f.readlines()
        for line in file:
            output = self._parse_line(line)
            if output is None:
                continue
            key, val = output
            if self.current_section == "kafka":
                if key == "brokers":
                    self.kafka.brokers = val
            elif self.current_section == "topic":
                if key == "in":
                    self.topic.in_ = val.split("\n")[0]
                elif key == "out_series":
                    self.topic.out_series = val.split("\n")[0]
                elif key == "out_properties":
                    self.topic.out_properties = val.split("\n")[0]
            elif self.current_section == "times":
                if key == "observation":
                    self.times.observations.append(int(val))
                elif key == "terminated":
                    self.times.terminated = int(val)
            elif self.current_section == "cascade":
                if key == "min_cascade_size":
                    self.cascade.min_cascade_size = int(val)

    def display_properties(self):
        print("[kafka]")
        print(f"    bokers={self.kafka.brokers}")
        print("[topic]")
        print(f"    in={self.topic.in_}", end="")
        print(f"    out_series={self.topic.out_series}", end="")
        print(f"    out_properties={self.topic.out_properties}")
        print("[times]")
        for o in self.times.observations:
            print(f"    observation={o}", end="")
        print(f"    terminated={self.times.terminated}")
        print("[cascade]")
        print(f"    min_cascade_size={self.cascade.min_cascade_size}")