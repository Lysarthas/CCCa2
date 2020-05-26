#!/usr/bin/env python

#  This file identifies the top 1500 negative and positive
#  corona-virus related tweets
#  A heap structure is used to track the top scores


from util import *

from collections import Counter
from crawler.util import get_db_client
from cloudant.result import Result
from mpi4py import MPI
import random
import sys
import couchdb

import heapq

db_config = load_config().get('db')
user = db_config.get('user')
password = db_config.get('password')
url = db_config.get('url')

couch = couchdb.Server('http://' + user + ':' + password + '@172.26.131.132:5984/')
top_sentiments_db = couch[db_config.get('top-sentiments-table')]
sentiments_db = couch[db_config.get('sentiments-table')]


def process(f):

    negative_heap = []
    heapq.heapify(negative_heap)

    positive_heap = []
    heapq.heapify(positive_heap)

    count = 0
    for item in f:
        print(count)
        count += 1
        pos_score = sentiments_db[item.id].get('pos_confidence_score')
        neg_score = sentiments_db[item.id].get('neg_confidence_score')
        try:
            if len(positive_heap) <= 1000:
                heapq.heappush(positive_heap, pos_score)
            else:
                min_value = positive_heap[0]
                if pos_score and pos_score > min_value:
                    heapq.heappop(positive_heap)
                    heapq.heappush(positive_heap, pos_score)

            if len(negative_heap) <= 1000:
                heapq.heappush(negative_heap, neg_score)
            else:
                min_value = negative_heap[0]
                if neg_score and neg_score > min_value:
                    heapq.heappop(negative_heap)
                    heapq.heappush(negative_heap, neg_score)
        except:
            print(sentiments_db[item.id])

    count = 0
    for item in f:
        print(count)
        pos_score = sentiments_db[item.id].get('pos_confidence_score')
        neg_score = sentiments_db[item.id].get('neg_confidence_score')

        try:
            if pos_score and pos_score >= positive_heap[0]:
                record = {
                          "tweet": sentiments_db[item.id].get('tweet'),
                          "place_name": sentiments_db[item.id].get('place_name'),
                          "place_full_name": sentiments_db[item.id].get('place_full_name'),
                          "place_type": sentiments_db[item.id].get('place_type'),
                          "author": sentiments_db[item.id].get('author'),
                          "post_at": sentiments_db[item.id].get('post_at'),
                          "confidence_score": pos_score,
                          "sentiment_code": 1,
                          "sentiment_type": 'positive'
                          }
                top_sentiments_db.save(record)

            if neg_score and neg_score >= negative_heap[0]:
                record = {
                          "tweet": sentiments_db[item.id].get('tweet'),
                          "place_name": sentiments_db[item.id].get('place_name'),
                          "place_full_name": sentiments_db[item.id].get('place_full_name'),
                          "place_type": sentiments_db[item.id].get('place_type'),
                          "author": sentiments_db[item.id].get('author'),
                          "post_at": sentiments_db[item.id].get('post_at'),
                          "confidence_score": neg_score,
                          "sentiment_code": 0,
                          "sentiment_type": 'negative'
                          }
                top_sentiments_db.save(record)
        except:
            print('error')
        count += 1


f = sentiments_db.view('_all_docs')
process(f)