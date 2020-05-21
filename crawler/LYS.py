#!/usr/bin/env python

from util import *
from cloudant.result import Result
from collections import Counter
from mpi4py import MPI

def get_db(db):

    db_result = get_db_client(db_name=db)
    view_result = db_result.get_view_result('_design/token-count', 'covid-tweets', reduce= True, stale='update_after')
    total_rows = view_result[0][0]['value']
    res_collection = db_result.get_view_result('_design/token-count', 'covid-tweets', reduce= False, stale='update_after')
    return res_collection, total_rows

def get_keywords():

    f = open("keyword.txt", "r", encoding='utf-8')
    kwd = []
    for line in f:
        kwd.append(line.rstrip('\n').lower())
    
    return kwd

def processor(f, task_rank, nodes, fsize):

    part = round(fsize / nodes)
    start = task_rank * part
    end = (task_rank + 1) * part
    if task_rank == (nodes - 1):
        end = fsize
    print("processor ", task_rank, " from ", start, " to ", end)

    keyword = get_keywords()
    counter = Counter()
    current = start

    while True:
        tweet = f[current][0]
        if tweet == '' or len(tweet) <= 2:
            break
        try:
            text = tweet['value']
            
            for words in keyword:
                if words in text:
                    counter[words] += 1
            
            current += 1
            if current >= end:
                break
        
        except:
            print('Error in parsing tweet :: ', tweet, ' ', len(tweet))
            break

    return counter

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# print("check", rank)
f, total_rows = get_db('junlin_id_fixed')
# print("processor", rank, " opened file, ", total_rows, " in total.")

kwd = processor(f, rank, size, total_rows)
keywords = comm.gather(kwd, root = 0)

if rank == 0:

    top = Counter()
    for k in keywords:
        top += k

    print(top)

