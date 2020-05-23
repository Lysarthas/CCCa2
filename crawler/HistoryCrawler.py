from util import *
from concurrent.futures import ThreadPoolExecutor, wait
import time
from datetime import datetime
import threading
from concurrent import futures
import gc

class HistoryCrawler:
    def __init__(self, api_list, start_date, end_date):
        super().__init__()

        self.tweet_db = get_db_client('junlin_id_fixed') ## tweet db
        self.finished_users_db = get_db_client('finished_user') ## db to store the users who has been crawled
        self.history_db = get_db_client('history_id_fixed')

        self.pool = ThreadPoolExecutor(max_workers=12)

        self.api_list = api_list
        self.start_date = start_date
        self.end_date = end_date

    def get_all_users(self):
        view_result = self.tweet_db.get_view_result('_design/result', 'user', group_level = 1, reduce=True, stable=False, update='lazy', raw_result=True)
        return [(row['key'], row['value']) for row in view_result['rows']]

    def get_finished_users(self):
        all_docs = self.finished_users_db.all_docs(include_docs=True)
        return dict([(row['key'], row['doc'].get('max_id')) for row in all_docs['rows']])

    def get_target_users(self):
        target_users = []
        finished_users = self.get_finished_users()

        all_users_results = self.get_all_users()
        for user_id, max_tweet_id in all_users_results:
            user_id = str(user_id)
            if user_id not in finished_users.keys():
                target_users.append((user_id, max_tweet_id))
            elif finished_users.get(user_id) is not None:
                target_users.append((user_id, min(int(max_tweet_id), int(finished_users[user_id]))))
        
        with open('progress', 'a') as f:
            f.write('total num of tasks: %d' % len(target_users))
        return target_users


    def run(self):
        self.target_users = self.get_target_users()
        all_tasks = []
        anchor = 0
        limit = 1000
        count = 0
        for user_id, max_id in self.target_users:
            api, auth = self.api_list[anchor]
            anchor = (anchor + 1) % len(self.api_list)
            all_tasks.append(self.pool.submit(self.craw_timeline, user_id, api, auth, max_id))
        
            if len(all_tasks) > limit:
                wait(all_tasks, return_when=futures.ALL_COMPLETED)
                count += limit
                del all_tasks[:]
                with open('progress', 'a') as f:
                    f.write('progress: %d / %d' % (count, len(self.target_users)))


    def createDoc(self, data):
        if str(data.id) in self.history_db: ## check duplicate
            # print("duplicate")
            return

        place = getattr(data, 'place')
        doc = {
            '_id': str(data.id_str),
            'post_at': data.created_at.timestamp(),
            'text': data.full_text,
            'json': data._json,
            'author': int(data.author.id_str),
            'place_name': place.name if place is not None else None,
            'place_full_name': place.full_name if place is not None else None,
            'place_type': place.place_type if place is not None else None
        }
        self.history_db.create_document(doc)
        del self.history_db[doc['_id']]

    def date_filter(self, tweets: list, create_doc_count: int):
        for status in tweets:
            if status.created_at < self.end_date and status.created_at > self.start_date:
                self.createDoc(status)
                create_doc_count += 1
            # elif status.created_at > self.end_date:
            #     print('%s too new' % status.created_at)
            # else:
            #     print('%s too old' % status.created_at)

        return create_doc_count

    def update_finished_user(self, user_id: str, max_id: int):
        if user_id in self.finished_users_db:
            doc = self.finished_users_db[user_id]
            doc['max_id'] = max_id
            doc.save()
        else:
            retry = 0
            while retry < 10:
                doc = self.finished_users_db.create_document({'_id': user_id, 'max_id': max_id})
                retry += 1
                if doc.exists():
                    del self.finished_users_db[user_id]
                    break
                

    def craw_timeline(self, user_id, api, auth, max_id):
        user_id = str(user_id)
        create_doc_count = 0
        max_id = str(max_id)

        while True:
            try:
                tmp_tweets = api.user_timeline(user_id, count = 200, include_rts=True, max_id = max_id, tweet_mode="extended")
                create_doc_count = self.date_filter(tmp_tweets, create_doc_count)

                if not tmp_tweets or len(tmp_tweets) < 200 or tmp_tweets[-1].created_at < self.start_date:
                    self.update_finished_user(user_id, None)
                    print("no more tweet")
                    break

                if create_doc_count > 500:
                    self.update_finished_user(user_id, None)
                    print("enough tweet")
                    break

                max_id = tmp_tweets[-1].id_str
                self.update_finished_user(user_id, max_id)

                time.sleep(5)
            except tweepy.RateLimitError:
                print('%s sleeping' % threading.get_ident())
                print(auth.access_token)
                sys.stdout.flush()
                time.sleep(15 * 60)
            except tweepy.TweepError as e:
                print(e.message[0]['message'])
                sys.stdout.flush()
                time.sleep(5)
            except:
                print("Unexpected error:", sys.exc_info()[0])
            finally:
                sys.stdout.flush()

        print("finish")
        sys.stdout.flush()

## api pool
accounts = config.get('accounts')
api_list = [init_api(name) for name in accounts]

## start date & end date
start_date = datetime(2020, 1, 10, 0, 0, 0)
end_date = datetime(2020, 5, 1, 0, 0, 0)

hc = HistoryCrawler(api_list, start_date, end_date)
hc.run()
