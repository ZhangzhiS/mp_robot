# -*- coding: utf-8 -*-
# JPG 16进制 FF D8 FF
# PNG 16进制 89 50 4e 47
# GIF 16进制 47 49 46 38
# 微信.bat 16进制 a1 86----->jpg  ab 8c----jpg     dd 04 --->png
# 自动计算异或 值
import os
from pathlib import Path
import sys
from enum import Enum



into_path = r'res'  # 微信image文件路径
out_path = r"tmp"


class ImgType(Enum):
    gif = 0x4749
    jpg = 0xFFD8
    png = 0x8950


class WechatConvert(object):

    @staticmethod
    def find_img_type(file_path):
        with open(file_path, 'rb') as f:
            byte1 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
            byte2 = int.from_bytes(f.read(1), byteorder=sys.byteorder)
        for img_enum in ImgType:
            png_tuple = WechatConvert.hex_to_tuple(img_enum.value)
            if png_tuple[0] ^ byte1 == png_tuple[1] ^ byte2:
                return img_enum.name, png_tuple[0] ^ byte1
        raise Exception("不支持的图片类型")

    @staticmethod
    def hex_to_tuple(img_type):
        return img_type >> 8, img_type & 0b11111111

    def convert(self, file_path):
        # 获取图片类型
        _,img_xor = WechatConvert.find_img_type(file_path)
        res = b""
        file_path = Path(file_path)
        with open(file_path, 'rb') as fd:
            while True:
                b = fd.read(1)
                if not b:
                    break
                real = int.from_bytes(b, byteorder=sys.byteorder) ^ img_xor

                real_bytes = int.to_bytes(real, 1, sys.byteorder)
                res += real_bytes
        return res


if __name__ == '__main__':
    res = WechatConvert().convert("./res/fca060dfcfa9ddc0f104f7badbda5992.dat")
