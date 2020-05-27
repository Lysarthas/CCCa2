from util import *
from cloudant.document import Document
from cloudant.result import Result
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import gc
from concurrent import futures
import os.path
from os import path

def update_finish_user_db(result, finished_users_db):
    result['value'] = str(result['value'])
    if result['key'] == result['value']:
        return
    
    if result['value'] in finished_users_db and result['key'] not in finished_users_db:
        doc = finished_users_db[result['value']]
        new_doc_dict = json.loads(doc.json())
        new_doc_dict.pop('_rev', None)
        new_doc['_id'] = result['key']
        new_doc = finished_users_db.create_document(new_doc_dict)
        if not new_doc.exists():
            print('create %s doc fail' % new_doc_dict['_id'])
        else:
            del finished_users_db[new_doc_dict['_id']] ## remove from loca cache
        doc.delete()

def update_user_id():
    db = get_db_client('junlin_id_fixed')
    result_collection = db.get_view_result('_design/result', 'user_id', reduce=False, stable=False, update='false')
    finished_users_db = get_db_client('finished_user')

    pool = ThreadPoolExecutor(max_workers=12)
    tasks = []
    limit = 10000
    count = 0
    for result in result_collection:
        if type(result) == 'list':
            print('result is list')
        tasks.append(pool.submit(update_finish_user_db, result, finished_users_db))
        if len(tasks) > limit:
            wait(tasks, return_when=futures.ALL_COMPLETED)
            count += limit
            print("finish %s jobs" % count)
            del tasks[:]
update_user_id()

# pool = ThreadPoolExecutor(max_workers=12)

# def fix_id(doc, target_db):
#     if doc['json']['id_str'] in target_db:
#         return
#     doc['_id'] = doc['json']['id_str']
#     doc['author'] = doc['json']['user']['id_str']
#     new_doc = target_db.create_document(doc)
#     if not new_doc.exists():
#         print("create fail: %s", new_doc['_id'])
#     else:
#         del target_db[new_doc['_id']]


# def read_startkey(file: str):
#     if not path.exists(file):
#         return ""

#     with open(file, 'r') as f:
#         return f.readline().strip()

# def write_startkey(file: str, startkey: str):
#     with open(file, 'w') as f:
#         f.write(startkey)

# count = 0
# file = 'startkey'
# for db_name in source_dbs:
#     source_db = get_db_client(db_name)
#     target_db = get_db_client(db_name + '_id_fixed')
#     tasks = []

#     limit = 50000
#     startkey = read_startkey(file)
#     result_collection = Result(source_db.all_docs, include_docs=True, endkey="_", startkey=startkey)
#     for result in result_collection:
#         doc = result['doc']
#         tasks.append(pool.submit(fix_id, doc, target_db))
#         if len(tasks) > limit:
#             wait(tasks, return_when=futures.ALL_COMPLETED)
#             count += limit
#             print("finish %s jobs" % count)
#             write_startkey(file, result['key'])
#             del tasks[:]
        



