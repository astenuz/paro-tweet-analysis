import tweepy
import logging
import json
import time
from sqlite3 import OperationalError
from pprint import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class StreamListener(tweepy.StreamListener):
    logger = logging.getLogger(__name__)

    def __init__(self,
                 api,
                 table):
        self.table = table
        self.api = api

    def on_status(self, status):
        logger.debug(status.text)
        # pprint(status._json)

        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        json_dump = json.dumps(status._json)

        if coords is not None:
            coords = json.dumps(coords)

        try:
            self.table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                json_dump=json_dump
                #             polarity=sent.polarity,
                #             subjectivity=sent.subjectivity,
            ))
        except:
            logger.error("could not save")
            time.sleep(0.5)

    def on_error(self, status_code):
        if status_code == 420:
            return False
