import os
import datetime
import tweepy
import dataset
import logging
from stream_listener import StreamListener

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)

# SECRETS
TWITTER_APP_KEY = os.environ['TWITTER_APP_KEY']
TWITTER_APP_SECRET = os.environ['TWITTER_APP_SECRET']

TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']

# initialize tweepy
auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

api = tweepy.API(auth)

# db_connection
db = dataset.connect("sqlite:///tweets.db")
table = db["tweets"]

# track on the following
track_on = ["#TODOESUNMONTAJEDELESTADO", "#teoriadelpanico", "#23NElParoSigue", "#Cacerolazo23N", "#ParoNacionalColombia"]

# run
stream_listener = StreamListener(api=api, table=table)
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=track_on)
