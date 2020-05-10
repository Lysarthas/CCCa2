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

        self.tweet_db = get_db_client() ## tweet db
        self.finished_users_db = get_db_client('finished_user') ## db to store the users who has been crawled
        self.history_db = get_db_client('history')

        self.pool = ThreadPoolExecutor(max_workers=8)

        self.api_list = api_list
        self.start_date = start_date
        self.end_date = end_date

    def get_all_users(self):
        view_result = self.tweet_db.get_view_result('_design/results', 'user', group_level = 1, raw_result=True, reduce=True)
        return [(row['key'], row['value']) for row in view_result['rows']]

    def get_finished_users(self):
        all_docs = self.finished_users_db.all_docs(include_docs=True)
        return dict([(int(row['key']), row['doc'].get('max_id')) for row in all_docs['rows']])

    def get_target_users(self):
        finished_users = self.get_finished_users()

        all_users = self.get_all_users()
        target_users = []
        for user, max_tweet_id in all_users:
            if user not in finished_users.keys():
                target_users.append((user, max_tweet_id))
            elif finished_users.get(user) is not None:
                target_users.append((user, min(max_tweet_id, finished_users[user])))
        return target_users


    def run(self):
        self.target_users = self.get_target_users()
        all_tasks = []
        anchor = 0
        limit = 500
        count = 0
        for user_id, max_id in self.target_users:
            api, auth = self.api_list[anchor]
            anchor = (anchor + 1) % len(self.api_list)
            all_tasks.append(self.pool.submit(self.craw_timeline, user_id, api, auth, max_id))
        
            if len(all_tasks) > limit:
                wait(all_tasks)
                del all_tasks[:]
                count += limit
                gc.collect()
                with open('progress', 'w') as f:
                    f.write('progress: %d / %d' % (count, len(self.target_users)))


    def createDoc(self, data):
        if str(data.id) in self.history_db: ## check duplicate
            # print("duplicate")
            return

        place = getattr(data, 'place')
        doc = {
            '_id': str(data.id),
            'post_at': data.created_at.timestamp(),
            'text': data.full_text,
            'json': data._json,
            'author': data.author.id,
            'place_name': place.name if place is not None else None,
            'place_full_name': place.full_name if place is not None else None,
            'place_type': place.place_type if place is not None else None
        }
        self.history_db.create_document(doc)
        del doc

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
            self.finished_users_db.create_document({'_id': user_id, 'max_id': max_id})

    def craw_timeline(self, user_id, api, auth, max_id):
        user_id = str(user_id)
        create_doc_count = 0

        while True:
            try:
                tmp_tweets = api.user_timeline(user_id, count = 200, include_rts=True, max_id = max_id, tweet_mode="extended")
                create_doc_count = self.date_filter(tmp_tweets, create_doc_count)

                if not tmp_tweets or len(tmp_tweets) < 10 or tmp_tweets[-1].created_at < self.start_date:
                    self.update_finished_user(user_id, None)
                    print("no more tweet")
                    break

                if create_doc_count > 400:
                    self.update_finished_user(user_id, None)
                    print("enough tweet")
                    break

                max_id = tmp_tweets[-1].id
                self.update_finished_user(user_id, max_id)
                
                del tmp_tweets[:]
                del tmp_tweets

                time.sleep(5)
            except tweepy.RateLimitError:
                print('%s sleeping' % threading.get_ident())
                time.sleep(15 * 60)
            except tweepy.TweepError as e:
                print(e.message[0]['message'])
                time.sleep(5)
            except Exception as e:
                print("Unexpected error:", str(e))
            except:
                print("Unexpected error:", sys.exc_info()[0])
            finally:
                sys.stdout.flush()

## api pool
accounts = config.get('accounts')
api_list = [init_api(name) for name in accounts]

## start date & end date
start_date = datetime(2020, 1, 10, 0, 0, 0)
end_date = datetime(2020, 5, 1, 0, 0, 0)

hc = HistoryCrawler(api_list, start_date, end_date)
hc.run()
