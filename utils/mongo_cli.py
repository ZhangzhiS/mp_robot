#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymongo import MongoClient

from settings import settings


def get_sync_conn():
    conn = MongoClient(settings.MONGODB_URL)
    db = conn[settings.MONGODB_DATABASE]
    # db.authenticate("wechat", "a5q0dOJ8")
    return db

sync_db = get_sync_conn()

def sync_get_skus(time_start):
    query = {"start_time": time_start, "activity_type": 21}
    objs = sync_db.jd_features.find(
        query, {"_id": 0}
    )
    return list(objs)

