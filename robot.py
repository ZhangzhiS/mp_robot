# -*- coding: utf-8 -*-
import enum
import websocket
import time
import json

from loguru import logger

from utils import tools
from settings import settings

SERVER = 'ws://127.0.0.1:5555'


def getid():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))


def log_print(msg):
    logger.info(msg)


class MessageType(enum.IntEnum):
    """消息类型"""
    HEART_BEAT = 5005
    RECV_TXT_MSG = 1
    RECV_PIC_MSG = 3
    USER_LIST = 5000
    GET_USER_LIST_SUCCSESS = 5001
    GET_USER_LIST_FAIL = 5002
    TXT_MSG = 555
    PIC_MSG = 500
    AT_MSG = 550
    CHATROOM_MEMBER = 5010
    CHATROOM_MEMBER_NICK = 5020
    PERSONAL_INFO = 6500
    DEBUG_SWITCH = 6000
    PERSONAL_DETAIL = 6550
    DESTROY_ALL = 9999


class RobotBase(object):

    def __init__(self) -> None:
        self.ws: websocket.WebSocketApp

    def on_open(self):
        pass

    def on_message(self, _):
        pass

    def on_error(self, _):
        pass
    
    def on_close(self):
        pass
    
    def heartbeat(self, _):
        pass

    def send_msg(
            self,
            msg_type: MessageType,
            msg: str,
            to_wxid: str,
            to_room_id: str,
            nickname: str,
        ):
        """
        给WS服务发送请求
        """
        msg_content = {
            'id': getid(),
            'type': msg_type.value,
            'content': msg,  # 文本消息内容
            'wxid': to_wxid,   # wxid,
            "roomid":to_room_id,
            "nickname":nickname,
            "ext":"null",
        }
        msg = json.dumps(msg_content)
        self.ws.send(msg)

    def send_text_msg(
            self,
            msg,
            to_wxid,
        ):
        """
        发送文本消息，wxid可以是用户id或者是群聊id
        """
        self.send_msg(
                MessageType.TXT_MSG,
                msg,
                to_wxid,
                to_room_id="null",
                nickname="null",
            )
    def send_img_msg(
            self,
            img_path,
            to_wxid
        ):
        """
        发送图片消息
        """
        self.send_msg(
                MessageType.PIC_MSG,
                img_path,
                to_wxid,
                to_room_id="null",
                nickname="null"
                )

    def get_user_list(self):
        """
        获取好友列表
        """
        self.send_msg(MessageType.USER_LIST, "user list", "null", "", "")


class WechatRobot(RobotBase):

    def __init__(self) -> None:
        super(RobotBase).__init__()
        # 需要转发的群
        self.forward_room_ids = []
        # 憨憨群
        self.happy_room_id = None
        # ws 连接
        self.wx = None
        # 优惠信息群
        self.group_name_complate_ids = []
        # 机器人找谱
        self.score_ids = []

    def on_message(self, message):
        recv_msg = json.loads(message)
        resp_type = recv_msg['type']
        action = {
            MessageType.CHATROOM_MEMBER_NICK: log_print,
            MessageType.PERSONAL_DETAIL: log_print,
            MessageType.AT_MSG: log_print,
            MessageType.DEBUG_SWITCH: log_print,
            MessageType.PERSONAL_INFO: log_print,
            MessageType.TXT_MSG: log_print,
            MessageType.PIC_MSG: log_print,
            MessageType.CHATROOM_MEMBER: log_print,
            MessageType.RECV_PIC_MSG: self.handle_img_msg,
            MessageType.RECV_TXT_MSG: self.handle_text_msg,
            MessageType.HEART_BEAT: self.heartbeat,
            MessageType.USER_LIST: self.handle_wxuser_list,
            MessageType.GET_USER_LIST_SUCCSESS: self.handle_wxuser_list,
            MessageType.GET_USER_LIST_FAIL: self.handle_wxuser_list,
        }
        action.get(resp_type, print)(recv_msg)
    
    def handle_wxuser_list(self, msg):
        """
        处理微信好友列表，记录需要转发的相关联系人的id
        """
        wx_user_list = msg["content"]
        for item in wx_user_list:
            wxid = item["wxid"] 
            if "@" in wxid:
                # 微信群
                if item["name"] == settings.TO_ROOM_NAME:
                    # 优惠信息转发
                    self.forward_room_ids.append(wxid)
                elif item["name"] == settings.GROUP_NAME_COMPLETE:
                    # 优惠信息来源
                    self.group_name_complate_ids.append(wxid)
                elif settings.SCORE_NAME_COMPLETE in item["name"]:
                    # 找谱群
                    self.score_ids.append(wxid)
            else:
                # 普通联系人，订阅号等
                pass

    def forward_discount_msg(self, text):
        """转发优惠信息"""
        res = ""
        urls = tools.get_urls(text)
        for url in urls:
            if "kuaizhan" in url:
                tb_url = tools.get_tb_url(url)
                if tb_url == url:
                    return
                new_url = tools.thief_url(tb_url)
            else:
                new_url = tools.thief_url(url)
            if not res:
                res = text.replace(url, new_url)
            else:
                res = res.replace(url, new_url)
        if res:
            for roomid in self.forward_room_ids:
                self.send_text_msg(res, roomid)

    def search_score(self, message):
        pass

    def handle_text_msg(self, msg):
        """
        处理收到的文本消息
        """
        message = msg.get("content")
        from_wxid = msg.get("wxid")
        if from_wxid in self.group_name_complate_ids:
            self.forward_discount_msg(message)

    def handle_img_msg(self, msg):
        """
        处理收到的图片消息
        """
        message = msg.get("content")
        from_wxid = msg.get("wxid")
        if from_wxid in self.score_ids:
            self.search_score(message)

    def run(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(SERVER,
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.run_forever()

    

robot = WechatRobot()
robot.run()
