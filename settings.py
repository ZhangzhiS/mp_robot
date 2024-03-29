#!/usr/bin/env python
# -*- coding: utf-8 -*-
# a5q0dOJ8
import json
from pathlib import Path
from typing import List


class Settings(object):
    
    GROUP_NAME: List[str] = ["今天coco挨打了吗"]  # 测试群聊
    GROUP_NAME_COMPLETE: str = "快乐x星球"
    # GROUP_NAME_COMPLETE: str = "coco"
    WECHATY_PUPPET_SERVICE_TOKEN: str = "python-wechaty-uos-token"
    WECHATY_PUPPET_SERVICE_ENDPOINT: str = "0.0.0.0:8080"
    TO_ROOM_NAME: str = "买买买"
    TO_ROOM_NAME1: str = "优惠线报"
    # TO_ROOM_NAMES: List[str] = ["优惠线报", "买买买"]
    # TO_ROOM_NAME: str = "test_jd"
    MONGODB_URL: str = "mongodb://wechat:a5q0dOJ8@82.156.173.222:27017/?authSource=jd"
    MONGODB_DATABASE: str = "jd"
    BLAKCLIST: List = []
    BLAKCLIST_PATH = "blacklist.txt"
    jd_api: str = "https://api.m.jd.com"
    cookies_path: str = "cookies.json"
    headers_path: str = "headers.json"

    cookies: dict = {}
    headers: dict = {}


    SCORE_NAME_COMPLETE: str = "机器人找谱"
    SEARCH_SCORE_HOST: str = "http://score-image-search-client.ai-k8s.xiaoyezi.com"
    WECHATY_PUPPET_SERVICE_TOKEN: str = "python-wechaty-uos-token"
    WECHATY_PUPPET_SERVICE_ENDPOINT: str = "0.0.0.0:8080"
    #WECHATY_LOG_FILE: str = "/data/logs/score-robot/score-robot-prod/robot.log"
    DSS_HOST: str = "https://dss.xiongmaopeilian.com/"
    TOKEN_FILE: str = "token.json"
    Y_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjMyNDksImV4cCI6MTY0ODg4ODM1NSwiaWF0IjoxNjQ2Mjk2MzU1LCJpc3MiOiJoenR1LmNuIiwic3ViIjoidXNlciB0b2tlbiJ9.egLTUelF0sTibLlO7LBUthuY-2pnNaVI7Pm2L5UjD9Y"
    
    wechat_path = Path("C:\\Users\\Administrator\\Documents\\WeChat Files")



settings = Settings()

settings.cookies = json.load(open(settings.cookies_path))
settings.headers = json.load(open(settings.headers_path))
settings.BLAKCLIST = [
        i.replace("\n", "") for i in open(
            settings.BLAKCLIST_PATH, encoding="utf-8"
        ).readlines()
    ]

