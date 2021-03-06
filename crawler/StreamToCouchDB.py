## Team members (Team 13):
## Yuansan Liu, 1037351
## Karun Varghese Mathew, 1007247
## Junlin Chen, 1065399
## Jingyi Shao, 1049816
## `Han Jiang, 1066425

from util import *


api, auth = init_api('mls')

class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super().__init__(api=api)
        self.db = get_db_client('junlin_id_fixed')

    def createDoc(self, data):
        if str(data.id) in self.db: ## check duplicate
            return

        place = getattr(data, 'place')

        is_truncated = data.truncated
        text = data.text
        if is_truncated:
            text = data.extended_tweet['full_text']
        doc = {
            '_id': str(data.id_str),
            'post_at': data.created_at.timestamp(),
            'text': text,
            'json': data._json,
            'author': int(data.author.id_str),
            'place_name': place.name if place is not None else None,
            'place_full_name': place.full_name if place is not None else None,
            'place_type': place.place_type if place is not None else None
        }
        self.db.create_document(doc)

    def on_status(self, status):
        self.createDoc(status)

    def on_error(self, status_code):
        print('Error::', status_code)
        return True

    def on_timeout(self):
        return True

## get new stream tweets
twitter_stream = tweepy.streaming.Stream(auth,TweetStreamListener())

australia_bound_box = get_location('australia')
australia_bound_box = australia_bound_box[0][::-1] + australia_bound_box[1][::-1]
twitter_stream.filter(locations=australia_bound_box)