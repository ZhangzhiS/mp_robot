#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


i = """
近期实测好吃的水果 🍈🍊

海南 玫珑蜜瓜网纹瓜3-4斤
券后价：19.8元
https://p.pinduoduo.com/vOP44FOY

广西 恭城脆柿出口大果5斤
券后价价：17.8元
https://p.pinduoduo.com/2Aq42D60

福建葡萄柚花皮大果5斤
券后价:  21.9元
https://p.pinduoduo.com/iGN4WgL5

赣南脐橙5斤特大果
券后价价：35.9元
https://p.pinduoduo.com/DPy4IC9F

上面四款水果都是买回来吃过之后分享给大家的，价格合适，味道也很好。

德亚 德国原装进口脱脂纯牛奶200ml*30盒
加入购物车1件
https://8narnis8.kuaizhan.com/?tkl=WJNGXAkRDDJ

凑单第1选项加入购物车1件
https://8narnis8.kuaizhan.com/?tkl=2h9FXAkTfM4
一起付款，德亚进口脱脂牛奶到手60.9元
"""
import json
import random
import requests

def get_data() -> str:
    data = json.load(open("data.json", "r"))
    s = random.choice(data)
    return s


def exchange_url(url: str):
    url = "https://api.youqiande.cn/tools/exchange_url"

    payload={'url': 'https://try.m.jd.com/1858710.html'}

    response = requests.request("POST", url, data=payload)
    print(response.json())


if __name__ == "__main__":
    # exchange_url("111")
    print(get_data())

