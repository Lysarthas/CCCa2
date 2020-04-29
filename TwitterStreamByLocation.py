import tweepy
import json

consumer_key = 'cGrAaG5mkE6t4wnBbcUJ3PlrY'
consumer_secret = 'm95G2ZzDoW45aQaK1KajBjYZBETtcWeJBkWNcuCoUgPJMbrWe4'
access_token = '1170264592410267648-eeYlYJuUBfcd1B0fsm0EibgrCYnSMM'
access_secret = 'tPq5g4FWN4xNxTyPANWdprpU4jeKBrmist2kniM5jXdmn'

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