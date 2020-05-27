#!/usr/bin/env python
## Team members (Team 13):
## Yuansan Liu, 1037351
## Karun Varghese Mathew, 1007247
## Junlin Chen, 1065399
## Jingyi Shao, 1049816
## `Han Jiang, 1066425

#   This file performs the actual classification of the tweets
#   It expects one or all of the classifier and tokenizer
#   model files to be available
#
#   The sentiment information along with relevant tweet data
#   is then stored in a separate table
#

from util import *

from collections import Counter
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from crawler.util import get_db_client
from keras.preprocessing.text import Tokenizer
from sklearn.linear_model import LogisticRegression
from cloudant.result import Result
from mpi4py import MPI
import random
import sys
import numpy as np
import pandas as pd
from joblib import dump, load
import couchdb

stopwords = set(stopwords.words('english'))
tweet_tokenizer = TweetTokenizer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

db_config = load_config().get('db')
user = db_config.get('user')
password = db_config.get('password')
url = db_config.get('url')
threshold_level = 0.999

couch = couchdb.Server('http://' + user + ':' + password + '@172.26.131.132/')
# sentiment data is stored to this table
sentiments_db = couch[db_config.get('sentiments-table')]


# get the covid related tweets view from couchdb
def get_db(db):
    db_result = get_db_client(db_name=db)
    view_result = db_result.get_view_result('_design/token', 'covid-tweets', reduce=True, stale='update_after')
    total_rows = view_result[0][0]['value']
    res_collection = db_result.get_view_result('_design/token', 'covid-tweets', reduce=False,
                                               stale='update_after')
    return res_collection, total_rows


# MPI code that runs parallely in the worker nodes
def processor(f, task_rank, nodes, fsize):
    part = round(fsize / nodes)
    start = task_rank * part
    end = (task_rank + 1) * part
    if task_rank == (nodes - 1):
        end = fsize
    print("processor ", task_rank, " from ", start, " to ", end)

    counter = Counter()
    current = start

    # load the pre-run logistic regression models
    classifier = load('classifier.joblib')
    tokenizer = load('tokenizer.joblib')

    while True:
        index = 0
        error = False
        records = []
        tweets = []
        while index < 1000 and current < end:
            view_record = f[current][0]
            if view_record == '' or len(view_record) <= 2:
                error = True
                break
            records.append(view_record['value'])
            text = view_record['value']['text']
            tweets.append(text)
            index += 1
            current += 1

        if current >= end:
            error = True

        tweet_test = tokenizer.texts_to_matrix(tweets, mode="count")
        # get the classification result
        predict_probability = classifier.predict_proba(tweet_test)
        index = 0

        # save the sentiment info along with relevant tweet data
        while index < len(predict_probability):
            record = {
                      "tweet": tweets[index],
                      "place_name": records[index]['place_name'],
                      "place_full_name": records[index]['place_full_name'],
                      "place_type": records[index]['place_type'],
                      "author": records[index]['author'],
                      "post_at": records[index]['post_at'],
                      "pos_confidence_score": predict_probability[index][1],
                      "neg_confidence_score": predict_probability[index][0]
                      }
            sentiments_db.save(record)
            index += 1
        if error:
            break

    return counter


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# db name hardcoded
f, total_rows = get_db('history_id_fixed')

kwd = processor(f, rank, size, total_rows)
keywords = comm.gather(kwd, root=0)

if rank == 0:

    top = Counter()
    for k in keywords:
        top += k

    print(top)

