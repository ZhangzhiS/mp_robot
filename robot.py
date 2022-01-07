# -*- coding: utf-8 -*-
import websocket
import time
import json

from utils import tools
from settings import settings

#SERVER = 'ws://192.168.9.113:5555'
SERVER = 'ws://127.0.0.1:5555'


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

def getid():
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

class WechatRobot(object):

    def __init__(self) -> None:
        # 需要转发的群
        self.forward_room_ids = []
        # 憨憨群
        self.happy_room_id = None
        # ws 连接
        self.wx = None
        # 优惠信息群
        self.group_name_complate_ids = []


    @staticmethod
    def get_chat_nick_p(roomid):
        qs = {
            'id': getid(),
            'type': CHATROOM_MEMBER_NICK,
            'content': roomid,
            'wxid': 'ROOT',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def debug_switch():
        qs = {
            'id': getid(),
            'type': DEBUG_SWITCH,
            'content': 'off',
            'wxid': 'ROOT',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def handle_nick(j):
        data = j.content
        i = 0
        for d in data:
            print(d.nickname)
            i += 1
    
    @staticmethod
    def hanle_memberlist(j):
        data = j.content
        i = 0
        for d in data:
            print(d.roomid)
            i += 1
    
    @staticmethod
    def get_chatroom_memberlist():
        qs = {
            'id': getid(),
            'type': CHATROOM_MEMBER,
            'wxid': 'null',
            'content': 'op:list member ',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def send_at_meg(roomid, nickname):
        qs = {
            'id': getid(),
            'type': AT_MSG,
            'roomid': roomid, # not null
            'content': '我能吞下玻璃而不伤身体',
            'nickname': '[微笑]Python',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def destroy_all():
        qs = {
            'id': getid(),
            'type': DESTROY_ALL,
            'content': 'none',
            'wxid': 'node',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def send_pic_msg():
        qs = {
            'id': getid(),
            'type': PIC_MSG,
            'content': 'C:\\Users\\14988\\Desktop\\temp\\2.jpg',
            'wxid': '获取的wxid',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def get_personal_detail():
        qs = {
            'id': getid(),
            'type': PERSONAL_DETAIL,
            'content': 'op:personal detail',
            'wxid': '获取的wxid',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def get_personal_info():
        qs = {
            'id': getid(),
            'type': PERSONAL_INFO,
            'content': 'op:personal info',
            'wxid': 'ROOT',
        }
        s = json.dumps(qs)
        return s
    
    @staticmethod
    def send_txt_msg(to_wxid, msg):
        '''
        发送消息给好友
        to_wxid 可以是roomid
        '''
        qs = {
            'id': getid(),
            'type': TXT_MSG,
            'content': msg,  # 文本消息内容
            'wxid': to_wxid   # wxid,
        }
        return json.dumps(qs)
    
    @staticmethod
    def send_wxuser_list():
        '''
        获取微信通讯录用户名字和wxid
        '''
        qs = {
            'id': getid(),
            'type': USER_LIST,
            'content': 'user list',
            'wxid': 'null',
        }
        s = json.dumps(qs)
        return s
    
    def handle_wxuser_list(self, j):
        j_ary = j['content']
        i = 0
        #微信群
        for item in j_ary:
            i += 1
            id = item['wxid']
            m = id.find('@')
            if settings.TO_ROOM_NAME == item["name"]:
                self.forward_room_ids.append(id)
            elif settings.GROUP_NAME_COMPLETE == item["name"]:
                self.group_name_complate_ids.append(id)
            if m != -1:
                print(i, id, item['name'])
        #微信其他好友，公众号等
        for item in j_ary:
            i += 1
            id = item['wxid']
            m = id.find('@')
            if m == -1:
                print(i, id, item['name'])
    
    def parse_msg(self, text):
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
        return res
    
    # @staticmethod
    def handle_recv_msg(self, msg):
        message = msg.get("content")
        from_wxid = msg.get("wxid")
        if from_wxid in self.group_name_complate_ids:
            # 处理转发优惠信息
            res = self.parse_msg(message)
            if res:
                for roomid in self.forward_room_ids:
                    self.ws.send.send_txt_msg(roomid, res)
        # if from_user == self.
        # self.ws.send(self.send_txt_msg())
    
    @staticmethod
    def heartbeat(j):
        pass
        # print(j['content'])
    
    
    # @staticmethod
    def on_open(self):
        self.ws.send(self.send_wxuser_list())     # 获取微信通讯录好友列表
    
    def on_message(self, message):
        j = json.loads(message)
        resp_type = j['type']
        action = {
            CHATROOM_MEMBER_NICK: self.handle_nick,
            PERSONAL_DETAIL: print,
            AT_MSG: print,
            DEBUG_SWITCH: print,
            PERSONAL_INFO: print,
            TXT_MSG: print,
            PIC_MSG: print,
            CHATROOM_MEMBER: self.hanle_memberlist,
            RECV_PIC_MSG: self.handle_recv_msg,
            RECV_TXT_MSG: self.handle_recv_msg,
            HEART_BEAT: self.heartbeat,
            USER_LIST: self.handle_wxuser_list,
            GET_USER_LIST_SUCCSESS: self.handle_wxuser_list,
            GET_USER_LIST_FAIL: self.handle_wxuser_list,
        }
        action.get(resp_type, print)(j)
    
    
    def on_error(self, error):
        print(error)
    
    
    def on_close(self):
        print("closed")

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
