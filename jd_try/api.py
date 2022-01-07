#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum
from typing import Dict, Any, Optional
from urllib.parse import urlencode


class METHOD(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseRequest:
    url: str
    method: METHOD
    params: Optional[Dict[str, Any]] = None
    json: Optional[Dict[Any, Any]] = None
    path_params: Optional[Dict[str, Any]] = None
    content: Optional[Any] = None


class TryFeedsList(BaseRequest):
    url = "client.action"
    method = METHOD.POST

    def __init__(self, tab_id, page):
        in_body = {
            "version": 2,
            "source": "default",
            "client": "outer",
            "previewTime": "",
            "page": page,
            "tabId": tab_id
        }
        body = {
            "functionId": "try_feedsList",
            "appid": "newtry",
            "uuid": "16348677660381223372083",
            "clientVersion": "",
            "client": "wh5",
            "osVersion": "13.2.3",
            "area": "",
            "networkType": "",
            "body": in_body
        }
        self.content = urlencode(body)


class GetTryDetails(BaseRequest):
    url = "client.action"
    method = METHOD.GET

    def __init__(self, try_id):
        in_body = {
            "activityId": try_id,
            "previewTime": ""
        }
        body = {
            "appid": "newtry",
            "functionId": "try_detail",
            "uuid": "16346349734491425543990",
            "clientVersion": "",
            "client": "wh5",
            "osVersion": "",
            "area": "",
            "networkType": "",
            "body": in_body
        }
        self.params = body
