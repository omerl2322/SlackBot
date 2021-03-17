from datetime import datetime

import slack
from flask import Flask, Response
from flask_apscheduler import APScheduler

from os_functions import pickle_in, pickle_out
from slack_bot import slack_token
from twitter_api.twitter_api import get_tweets_from_last_x

app = Flask(__name__)
scheduler = APScheduler()


def send_tweets_to_slack(time_frame):
    counter = 0
    client = slack.WebClient(token=slack_token)
    tweets_from_last_x = get_tweets_from_last_x(time_frame)
    for tweet in tweets_from_last_x:
        content_list = pickle_out('content_list')
        if tweet.tweet_id in content_list:
            counter = +1
        else:
            content_list.append(tweet.tweet_id)
            pickle_in('content_list', content_list)
            message = str(datetime.now().replace(microsecond=0)) + '-' + tweet.url
            client.chat_postMessage(channel='#content', text=message)
    if len(tweets_from_last_x) == 0 or len(tweets_from_last_x) == counter:
        client.chat_postMessage(channel='#content', text='There are no new tweets')


def scheduled_task():
    print('this task is running every 60 minutes')
    send_tweets_to_slack('last_hour')
    pass


@app.route('/now', methods=['POST'])
def now_res():
    send_tweets_to_slack('now')
    return Response(), 200


@app.route('/new-content', methods=['POST'])
def new_content_res():
    send_tweets_to_slack('last_hour')
    return Response(), 200


if __name__ == "__main__":
    scheduler.add_job(id='Scheduled task', func=scheduled_task, trigger='interval', hours=1)
    scheduler.start()
    app.run(debug=True)
