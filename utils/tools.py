#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import requests
import random

from loguru import logger
import ahocorasick  # noqa

from settings import settings

def build():
    trie = ahocorasick.Automaton()
    for index, word in enumerate(settings.BLAKCLIST):
        trie.add_word(word, (index, word))
    trie.make_automaton()
    return trie


def check_blacklist(title, matcher):
    black_status = False
    for black_item in matcher.iter(title):
        if black_item:
            black_status = True
            continue
    return black_status

type_map = {
    "pdd": "pdd_good_info",
    "jd": "jd_good_info",
    "sn": "sn_good_info",
    "tb": "tb_good_info",
}


def get_urls(text: str):
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
    return urls


def suowo_url(url: str):
    api = "https://urll.ink/api/links"
    payload={'longUrl': url}
    response = requests.request("POST", api, data=payload)
    return response.json().get("data", {}).get("code")


def exchange_url(url: str):
    api = "https://api.youqiande.cn/tools/exchange_url"
    logger.info(url)
    # url = "https://try.m.jd.com/1859022.html"

    payload={'url': url}

    response = requests.request("POST", api, data=payload)
    if response.status_code == 200:
        logger.info(response.text)
        jd_url = response.json().get("data", "")
        jd_url = get_urls(jd_url)
        if jd_url:
            jd_url = jd_url[0]
        logger.info(jd_url)
        yqd_api = "https://api.youqiande.cn/goods/url"
        data = {
            "urls": [jd_url]
        }
        token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjMyNDksImV4cCI6MTY0MTY5OTU3NCwiaWF0IjoxNjM5MTA3NTc0LCJpc3MiOiJoenR1LmNuIiwic3ViIjoidXNlciB0b2tlbiJ9.DgVrbjFjONk9bHKoNYsF055sNWRq1qUZJZ_S6l7LUTU"
        headers = {
            "authorization": token,
            'Content-Type': 'application/json',
        }
        res = requests.post(yqd_api, json=data, headers=headers)
        if res.status_code == 200:
            url = res.json().get("data", {}).get("jd_good_info", {}).get("url", "")
            if url:
                return suowo_url(url)
    return ""


def get_tb_url(url: str):
    tkl = url.split("tkl=")[-1]
    yqd_tp_api = "https://api.youqiande.cn/goods/tp"
    data = {"content": tkl}
    res = requests.post(yqd_tp_api, json=data)
    new_url = res.json().get("data", {}).get("url", "")
    return new_url


def thief_url(url: str):
    yqd_api = "https://api.youqiande.cn/goods/url"
    data = {
        "urls": [url]
    }
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOjMyNDksImV4cCI6MTY0MTY5OTU3NCwiaWF0IjoxNjM5MTA3NTc0LCJpc3MiOiJoenR1LmNuIiwic3ViIjoidXNlciB0b2tlbiJ9.DgVrbjFjONk9bHKoNYsF055sNWRq1qUZJZ_S6l7LUTU"
    headers = {
        "authorization": token,
        'Content-Type': 'application/json',
    }
    res = requests.post(yqd_api, json=data, headers=headers)
  
    if res.status_code != 200:
        return url
    data = res.json().get("data")
    good_type = data.get("type")
    if not type:
        return url
    good_info = data.get(type_map.get(good_type, "not_fond"), {})
    print(good_info)
    if not good_info:
        return url
    good_name = good_info.get("goods_name")
    if not good_name:
        return url
    if good_type == "tb":
        tpwd = good_info.get("tpwd")
        tmp = re.findall(r"￥(.*?)￥", tpwd)
        tkl = tmp[0] if tmp else None
        new_url = f"https://8narnis8.kuaizhan.com/?tkl={tkl}"
        return new_url
    new_url = good_info.get("url")
    print(good_info)
    if not new_url:
        return url
    return new_url


def get_data() -> str:
    f = open("data.json", "r")
    data = json.load(f)
    s = random.choice(data)
    return s


