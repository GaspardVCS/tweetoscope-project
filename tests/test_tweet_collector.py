import sys
sys.path.append("..")
from tweet_collector.tweet import Tweet

def addition(a, b):
    return a + b

def test_fake_function():
   assert addition(1, 1) == 2
   assert addition(1, -1) == 0