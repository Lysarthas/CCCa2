import tweepy
import json

consumer_key = 'h1dqkm4wP9vui7U3snEMS0Z6A'
consumer_secret = 'm20fMBT1Ijx7yNS9PXf8hSmYix8TgkkNtp3YHin0EO7UWiROFZ'
access_token = '1170264592410267648-SZUOk09ew5EAURbUcPvEi4PoyCGMB0'
access_secret = 'EsgTim4FkLeYxmjX1baOUKbeGgj2YDwf2BknHkxLr1Tfu'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


class TweetStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status._json)
        f = open("tweets.json", "a")
        f.write('\n' + json.dumps(status._json))
        f.close()

    def on_error(self, status_code):
        print('Error::', status_code)
        return True

    def on_timeout(self):
        return True


twitter_stream = tweepy.streaming.Stream(auth,TweetStreamListener())
twitter_stream.filter(locations=[113.1, -38.2, 158.7, -23.3])