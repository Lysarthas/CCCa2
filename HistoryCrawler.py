from util import *
from concurrent.futures import ThreadPoolExecutor, wait
import time
import numpy as np
from numpy.random import choice
import datetime

class HistoryCrawler:
    def __init__(self, api_list, start_date, end_date):
        super().__init__()

        self.tweet_db = get_db_client() ## tweet db
        self.finished_users_db = get_db_client('finished_user') ## db to store the users who has been crawled
        self.history_db = get_db_client('history')

        self.pool = ThreadPoolExecutor(max_workers=4)

        self.api_list = api_list
        self.api_select_count = np.ones(len(self.api_list), dtype=np.int)
        self.start_date = start_date
        self.end_date = end_date

    def get_all_users(self):
        view_result = self.tweet_db.get_view_result('_design/results', 'user', group_level = 1, raw_result=True)
        return [row['key'] for row in view_result['rows']]

    def get_finished_users(self):
        all_docs = self.finished_users_db.all_docs()
        return [int(row['key']) for row in all_docs['rows']]

    def get_target_users(self):
        finished_users = self.get_finished_users()
        all_users = self.get_all_users()
        return list(set(all_users) - set(finished_users))

    def run(self):
        self.target_users = self.get_target_users()
        all_tasks = []
        for user_id in self.target_users:
            probability_distribution = 1 - self.api_select_count / sum(self.api_select_count)
            draw = choice(range(len(self.api_list)), 1, p=probability_distribution)[0]
            self.api_select_count[draw] += 1
            api, auth = self.api_list[draw]
            all_tasks.append(self.pool.submit(self.craw_timeline, user_id, api, auth))
        wait(all_tasks)

    def createDoc(self, data):
        if str(data.id) in self.history_db: ## check duplicate
            return

        place = getattr(data, 'place')

        is_truncated = data.truncated
        text = data.text
        if is_truncated:
            text = data.extended_tweet['full_text']
        doc = {
            '_id': str(data.id),
            'post_at': data.created_at.timestamp(),
            'text': text,
            'json': data._json,
            'author': data.author.id,
            'place_name': place.name if place is not None else None,
            'place_full_name': place.full_name if place is not None else None,
            'place_type': place.place_type if place is not None else None
        }
        self.history_db.create_document(doc)

    def date_filter(self, tweets: list):
        for status in tweets:
            if status.created_at < self.end_date and status.created_at > self.start_date:
                self.createDoc(status)

    def craw_timeline(self, user_id, api, auth):
        max_id = -1
        is_finished = False
        tmp_tweets = []
        user_id = str(user_id)

        while not is_finished:
            try:
                if max_id < 0 or not tmp_tweets:
                    tmp_tweets = api.user_timeline(user_id)
                    self.date_filter(tmp_tweets)
                    max_id = tmp_tweets[-1].id
                    time.sleep(10)

                while (tmp_tweets and tmp_tweets[-1].created_at > self.start_date):
                    tmp_tweets = api.user_timeline(user_id, max_id = max_id)
                    self.date_filter(tmp_tweets)
                    max_id = tmp_tweets[-1].id
                    time.sleep(10)
                
                ## mark the user finished
                self.finished_users_db.create_document({'_id': user_id})
                is_finished = True
            except tweepy.RateLimitError:
                time.sleep(15 * 60)

## api pool
api1, auth1 = init_api('karun')
api2, auth2 = init_api('jinyi')
api_list = [(api1, auth1), (api2, auth2)]

## start date & end date
start_date = datetime.datetime(2020, 1, 20, 0, 0, 0)
end_date = datetime.datetime(2020, 5, 1, 0, 0, 0)


hc = HistoryCrawler(api_list, start_date, end_date)
hc.run()
