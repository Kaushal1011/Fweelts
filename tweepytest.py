import sys
import tweepy
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # if 'manchester united' in status.text.lower():
        print(status.text)

    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())    
sapi.filter(locations=[-6.38,49.87,1.77,55.81])
