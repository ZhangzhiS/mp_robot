#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import httpx

from jd_try import api
from jd_try.api import BaseRequest


class BaseClient:
    def __init__(self, cookies, headers, host, client):
        self._host = host
        self.cookies = cookies
        self.headers = headers
        self.cli = client

    def prepare(self, request: BaseRequest) -> httpx.Request:
        url = os.path.join(self._host, request.url)
        req = httpx.Request(
            method=request.method.value,
            url=url,
            cookies=self.cookies,
            headers=self.headers,
            params=request.params,
            content=request.content,
        )
        req.read()
        return req


class SyncClient(BaseClient):

    def request(self, req: BaseRequest):
        prepared_req = self.prepare(req)
        resp = self.cli.send(prepared_req)
        if resp.status_code == 200:
            return json.loads(resp.text)
        return {}

    def get_feeds_list(self, tab_id, page):
        return self.request(api.TryFeedsList(tab_id, page))

    def get_try_details(self, try_id):
        return self.request(api.GetTryDetails(try_id))


class AsyncClient(BaseClient):

    async def request(self, req: BaseRequest):
        prepared_req = self.prepare(req)
        resp = await self.cli.send(prepared_req)
        if resp.status_code == 200:
            return json.loads(resp.text)
        return {}

    async def get_feeds_list(self, tab_id, page):
        return await self.request(api.TryFeedsList(tab_id, page))

    async def get_try_details(self, try_id):
        return await self.request(api.GetTryDetails(try_id))


if __name__ == '__main__':
    cookies_t: dict = json.load(open("../config/cookies.json"))
    headers_t: dict = json.load(open("../config/headers.json"))
    with httpx.Client() as cli:
        c = SyncClient(cookies_t, headers_t, "https://api.m.jd.com", cli)
        print(c.get_try_details(1795699))
