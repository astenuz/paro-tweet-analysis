import os
import datetime
import pandas as pd
import tweepy
import dataset
import logging
from stream_listener import StreamListener

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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

# track on trends
trends = pd.DataFrame.from_records(
    api.trends_place(368148)[0]['trends'])
# trends = trends.loc[trends.name.str.startswith('#')].head(15)
trends = trends.head(20)


# track on the following
# track_on = ["#TODOESUNMONTAJEDELESTADO", "#teoriadelpanico", "#23NElParoSigue", "#Cacerolazo23N", "#ParoNacionalColombia"]
track_on = trends.name.values.tolist()

logger.info("tracking on: {}".format(track_on))

# run
stream_listener = StreamListener(api=api, table=table)
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=track_on)
