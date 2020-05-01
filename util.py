import json
import tweepy
from collections import namedtuple
from cloudant.client import Cloudant

config_file = 'config.json'

def load_config():
    with open(config_file, 'rb') as f:
        config = json.loads(f.read())
        return config

config = load_config()

def get_account(key: str):
    return config.get('accounts').get(key)


def get_location(location: str):
    return config.get("target_location").get(location)

def get_db_client(db_name: str = None):
    db_config = config.get('db')
    user = db_config.get('user')
    passwd = db_config.get('password')
    url = db_config.get('url')
    client = Cloudant(user, passwd, url=url, connect=True, auto_renew=True)
    db_name = db_config.get('db') if db_name is None else db_name
    return client[db_name]

def init_api(account_key: str):
    account = get_account(account_key)

    consumer_key = account.get('consumer_key')
    consumer_secret = account.get('consumer_secret')
    access_token = account.get('access_token')
    access_token_secret = account.get('access_token_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth), auth


covid_keyword_file = 'covid_keyword.txt'
def get_covid_track():
    tracks = []
    with open(covid_keyword_file, 'r') as f:
        for line in f:
            tracks.append(line.strip())
    return tracks