#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
优惠线报机器人
https://api.youqiande.cn/tools/exchange_url
"""
import json
import re
import os
import datetime
import asyncio
import random
from typing import Optional

import requests
# import httpx
from wechaty import Wechaty, Contact, RoomQueryFilter
from wechaty.user import Message
from wechaty_puppet import MessageType, ScanStatus
from loguru import logger

from settings import settings
from mongo_cli import sync_get_skus
from jd_try.client import AsyncClient
from tools import build, check_blacklist


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
    if not new_url:
        return url
    return new_url


def get_data() -> str:
    f = open("data.json", "r")
    data = json.load(f)
    s = random.choice(data)
    return s


class WechatRobot(Wechaty):
    """
    微信机器人
    """

    def __init__(self):
        self.login_user: Optional[Contact] = None
        super().__init__()

    def parse_msg(self, text):
        res = ""
        urls = get_urls(text)
        for url in urls:
            if "kuaizhan" in url:
                tb_url = get_tb_url(url)
                if tb_url == url:
                    return
                new_url = thief_url(tb_url)
            else:
                new_url = thief_url(url)
            if not res:
                res = text.replace(url, new_url)
            else:
                res = res.replace(url, new_url)
        return res

    async def forward_msg(self, msg):
        to_room = await self.Room.find(RoomQueryFilter(topic=settings.TO_ROOM_NAME))
        if not to_room:
            return
        await to_room.say(msg)

    async def jd_work(self, room_name=settings.TO_ROOM_NAME):
        logger.info(f"init {room_name}")
        while True:
            to_room = await self.Room.find(RoomQueryFilter(topic=room_name))
            if not to_room:
                await asyncio.sleep(2)
                continue
            jd_now = requests.get("https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5").json()
            now = datetime.datetime.now()
            next_hour = now + datetime.timedelta(hours=1)
            push_data = datetime.datetime(
                next_hour.year, next_hour.month, next_hour.day, next_hour.hour
            )
            push_timestamp = int(push_data.timestamp())

            try:
                sleep_time = push_timestamp - int(jd_now.get("currentTime2"))/1000
            except:
                continue
            logger.info(sleep_time)
            logger.info(push_timestamp)

            await asyncio.sleep(sleep_time)
            skus = sync_get_skus(push_timestamp*1000)
            matcher = build()
            if skus:
                for i in skus:
                    try_id = i.get("try_id")
                    sku_title = i.get("sku_title")
                    if check_blacklist(sku_title, matcher):
                        continue
                    price = i.get("price")
                    order_price = i.get("order_price")
                    try_url = f"https://try.m.jd.com/{try_id}.html"
                    try_url = exchange_url(try_url)
                    if not try_url:
                        continue
                    desc = f"""京东付费试用
按照自己的需要进行购买，注意价格是否合适，有不少特别便宜的东西
-------------------
{sku_title}
-------------------
试用价：{order_price}
原价：{price} 
试用链接地址：{try_url}
"""
                    if to_room:
                        await to_room.say(desc)
            await asyncio.sleep(58*60)

    async def on_message(self, msg: Message):
        """
        消息监听
        """
        # 获取发送消息的用户
        from_contact = msg.talker()
        if from_contact.is_self():
            # 机器人回复的图片不进行搜索
            return
        # 获取消息来源是否是群
        room = msg.room()
        if not room:
            if from_contact.name == "张智":
                if msg.type() != MessageType.MESSAGE_TYPE_TEXT:
                    u = exchange_url(msg.text())
                    if u:
                        await from_contact.say(u)
                    return
                await msg.ready()
                text = msg.text()
                res = self.parse_msg(text)
                if not res:
                    return
                await from_contact.say(res)
                await self.forward_msg(res)
            return
        await room.ready()
        room_name = await room.topic()
        if not room_name:
            return
        if settings.GROUP_NAME_COMPLETE not in room_name:
            if from_contact.name != "@":
                return
            await msg.ready()
            text = msg.text()
            if "分手" in text:
                logger.info(from_contact.name)
                m = get_data()
                await msg.say(m)
                # await msg.say("你要实在没事干，找个班上吧，人闲了就容易胡思乱想")
            elif "复合" in text:
                await msg.say("好马不吃回头草")
            elif "前女友" in text:
                await msg.say("你现女友都没有了")
            return
        if msg.type() != MessageType.MESSAGE_TYPE_TEXT:
            return
        await msg.ready()
        text = msg.text()
        res = self.parse_msg(text)
        if not res:
            return
        await self.forward_msg(res)

    async def on_login(self, contact: Contact):
        """
        监听登录事件
        """
        self.login_user = contact
        await self.jd_work()

    async def on_scan(
            self,
            status: ScanStatus,
            qr_code: Optional[str],
            data: Optional[str] = None
            ):
        """
        扫码事件监听
        如果已经登录了，则不会触发
        """
        contact = self.Contact.load(self.contact_id)
        await contact.ready()
        print(f"用户 <{contact}> scan status: {status.name}")
        print(f"qr_code: {qr_code}")


bot: Optional[WechatRobot] = None


async def main():
    global bot
    bot = WechatRobot()
    await bot.start()

if __name__ == "__main__":
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = settings.WECHATY_PUPPET_SERVICE_TOKEN
    os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = settings.WECHATY_PUPPET_SERVICE_ENDPOINT
    os.environ['WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_CLIENT'] = "true"
    asyncio.run(main())
