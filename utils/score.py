import os
import time
import json
import requests
from settings import settings
from loguru import logger


class SearchError(Exception):
    pass


class DssClient(object):
    """请求dss的接口"""

    @classmethod
    def get_score(cls, data):
        uri = "student_app/opn/music_score_search"
        url = settings.DSS_HOST+uri
        with open(settings.TOKEN_FILE, "r") as f:
            info = json.load(f)
        token = info.get("data").get("token")
        headers = {"token": token, "version": "1"}
        logger.info(url)
        resp = requests.post(url, json=data, headers=headers)
        logger.info(resp)
        if resp.status_code != 200:
            raise SearchError("DSS 相关服务异常")
        result = resp.json()
        if result.get("code") == 1:
            data = result.get("data")
            if data:
                err = data.get("errors")
                raise SearchError(str(err))
            err = result.get("errors")[0].get("err_msg")
            raise SearchError(err)
        return result

    @classmethod
    def login(cls, mobile):
        """登录接口"""
        uri = "student_app/auth/login"
        url = os.path.join(settings.DSS_HOST, uri)
        code = input("请输入手机验证码：")
        data = {
            "mobile": mobile,
            "code": code
        }
        resp = requests.post(url, data=data)
        if resp.status_code != 200:
            return
        result = resp.json()
        with open(settings.TOKEN_FILE, "w") as f:
            json.dump(result, f)
        return result

    @classmethod
    def get_validate_code(cls, phone):
        """获取验证码"""
        uri = "student_app/auth/validate_code"
        url = os.path.join(settings.DSS_HOST, uri)
        resp = requests.get(url, params={"mobile": phone, "country_code": 86})
        if resp.status_code != 200:
            return
        result = resp.json()
        return result
    
    @classmethod
    def search_score(cls, image):
        """搜索曲谱：上传图片接口"""
        files = {"file": image}
        data = {
            'sourceId': 1,
        }
        resp = requests.post(
            settings.SEARCH_SCORE_HOST+"/ai/score/img/upload",
            data=data,
            files=files
        )
        if resp.status_code != 200:
            raise SearchError("曲谱搜索服务异常")
        res = resp.json()
        if res.get("code") == 1:
            raise SearchError(res.get("message"))
        data = res.get("data")
        get_search_count = 0
        image_list = []
        data.update({
            "isUrl": 0,
            "sourceId": 1,
            "requestType": 0
        })
        search_result = {}
        while get_search_count < 10:
            search_result_resp = requests.get(
                    settings.SEARCH_SCORE_HOST+"/ai/score/img/search/result",
                    params=data
            )
            if search_result_resp.status_code != 200:
                raise SearchError("获取搜索结果失败")
            search_result = search_result_resp.json()
            record_id = search_result.get("data").get("record_id")
            if record_id == 0:
                time.sleep(1)
                get_search_count += 1
                continue
            image_list = search_result.get("data").get("images")
            break
        if not image_list:
            raise SearchError("未搜索到该曲谱")
        return search_result.get("data")

    @classmethod
    def download_img_local(cls, url):
        content = requests.get(url).content
        file = f"{int(time.time())}.jpg"
        new_path = os.path.join(os.getcwd(), "tmp")
        new_path = os.path.join(new_path, file)
        with open(new_path, "wb") as w:
            w.write(content)
        return new_path

