#!/usr/bin/env python
# -*- coding: utf-8 -*-
# a5q0dOJ8
import json
from typing import List


class Settings(object):
    
    GROUP_NAME: List[str] = ["今天coco挨打了吗"]  # 测试群聊
    # GROUP_NAME_COMPLETE: str = "快乐x星球"
    GROUP_NAME_COMPLETE: str = "coco"
    WECHATY_PUPPET_SERVICE_TOKEN: str = "python-wechaty-uos-token"
    WECHATY_PUPPET_SERVICE_ENDPOINT: str = "0.0.0.0:8080"
    # TO_ROOM_NAME: str = "优惠线报"
    TO_ROOM_NAME: str = "to_test"
    MONGODB_URL: str = "mongodb://wechat:a5q0dOJ8@82.156.173.222:27017/?authSource=jd"
    MONGODB_DATABASE: str = "jd"
    BLAKCLIST: List = []
    BLAKCLIST_PATH = "/home/ubuntu/projecr/robot/blacklist.txt"
    jd_api: str = "https://api.m.jd.com"
    cookies_path: str = "/home/ubuntu/projecr/robot/cookies.json"
    headers_path: str = "/home/ubuntu/projecr/robot/headers.json"

    cookies: dict = {}
    headers: dict = {}


settings = Settings()

settings.cookies = json.load(open(settings.cookies_path))
settings.headers = json.load(open(settings.headers_path))
settings.BLAKCLIST = [
        i.replace("\n", "") for i in open(
            settings.BLAKCLIST_PATH, encoding="utf-8"
        ).readlines()
    ]

