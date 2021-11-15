import argparse
from tweetoscopeCollectorParams import TweetoscopeCollectorParams

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("param_file_path", help="Path to the collector parameters file")
args = parser.parse_args()
collector = TweetoscopeCollectorParams(args.param_file_path)

if __name__ == "__main__":
    collector.display_properties()