import datetime
import json
from datetime import datetime, timedelta

import dateutil.parser
import pytz
import requests

from twitter_api import Bearer_token, twitter_accounts

utc = pytz.UTC
tweets_obj = []


# ----------------------------------------------------------------------------------------------------------------------
def create_tweet_obj_list(tweets_dic, user_name):
    for item in tweets_dic:
        time_stamp = handle_time_stamp(item['created_at'])
        tweets_obj.append(Tweet(item['id'], time_stamp, user_name))


# ----------------------------------------------------------------------------------------------------------------------
def get_tweets_from_last_x(time_frame):
    filter_tweets = []
    for item in twitter_accounts:
        user_id = twitter_accounts[item]
        create_tweet_obj_list(get_tweets(user_id), item)
    if time_frame == 'last_hour':
        filter_tweets = [item for item in tweets_obj if item.created_last_hour()]
        print(filter_tweets)
    elif time_frame == 'now':
        filter_tweets = [item for item in tweets_obj if item.created_now()]
        print(filter_tweets)
    return filter_tweets


# ----------------------------------------------------------------------------------------------------------------------
# Returns the most recent Tweets composed by a single user specified by the requested user ID.
def get_tweets(user_id):
    try:
        url = 'https://api.twitter.com/2/users/' + user_id + '/tweets?tweet.fields=created_at'
        headers = {
            'Authorization': Bearer_token
            # 'Cookie': 'guest_id=v1%3A161597629902057889; personalization_id="v1_1hkZz5Jdio9fXFx+v8Vf2w=="'
        }
        response = requests.request("GET", url, headers=headers)
        t = json.loads(response.text)['data']
        return json.loads(response.text)['data']
    except requests.RequestException as e:
        print(e)
        # need to handle issue
        return None


# ----------------------------------------------------------------------------------------------------------------------
# convert date (ISO 8601) to datetime
def handle_time_stamp(string_timestamp):
    new_timestamp = dateutil.parser.parse(string_timestamp)
    return new_timestamp


# ----------------------------------------------------------------------------------------------------------------------
class Tweet:

    def __init__(self, tweet_id, tweet_created_at, user_name):
        self._tweet_id = tweet_id
        self._tweet_created_at = tweet_created_at
        self._url = 'https://twitter.com/' + user_name + '/status/' + tweet_id

    @property
    def tweet_id(self):
        return self._tweet_id

    @property
    def tweet_created_at(self):
        return self._tweet_created_at

    @property
    def url(self):
        return self._url

    def created_last_hour(self):

        current_time = datetime.now().replace(tzinfo=utc)
        an_hour_ago = (datetime.now() + timedelta(hours=-3)).replace(tzinfo=utc)
        created_at = self.tweet_created_at
        if an_hour_ago < created_at < current_time:
            return True
        return False

    def created_now(self):
        a_minute_ago = (datetime.now() + timedelta(minutes=-1)).replace(tzinfo=utc)
        if self.tweet_created_at > a_minute_ago:
            return True
        return False
