#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''工具类'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import random
import time
import platform
import hashlib
import hmac
import base64
import re
import json

from src.config import BaseConfig

# import qrcode

STR = [
    '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'a', 'b',
    'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
]

NUM = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

CHARS = [
    "a", "b", "c", "d", "e", "f", "g", "h",
    "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H",
    "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]


def hmac_sha_256(msg, key):
    message = bytes(msg).encode('utf-8')
    secret = bytes(key).encode('utf-8')

    signature = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    print(signature)
    return signature
    pass


def get_value(url, key):
    """
    通过截取的方式获取url中的拼接参数
    :param url:
    :param key:
    :return:
    """
    if url is None or url == "":
        return None

    key = key + "="

    if key not in url:
        return None

    index = url.index(key)

    if index != -1:
        url = url[index + len(key):len(url)]
        pass

    if "&" not in url:
        return url

    index = url.index("&")

    if index != -1:
        url = url[0:index]
        pass
    return url
    pass


def get_id():
    """
    获取不重复的id
    :return:
    """
    # print u"操作系统名称及版本号: ",platform.platform(),hash(platform.platform())
    # print u"操作系统的位数: ",platform.architecture(),hash(platform.architecture())
    # print u"计算机类型: ", platform.machine(),hash(platform.machine())
    # print u"计算机的网络名称: ", platform.node(),hash(platform.node())
    # print u"计算机处理器信息: ", platform.processor(),hash(platform.processor())

    mache_id = hash(platform.platform()) ^ hash(platform.architecture()) ^ hash(
        platform.machine()) ^ hash(
        platform.node()) ^ hash(platform.processor())
    time_ = int(time.time())
    rand = int(random.uniform(1000, 60000))
    # print hex(60000)

    id = "%s%s" % ('{:x}'.format(mache_id), '{:x}'.format(time_ ^ rand))
    # print id
    return id
    pass


def get_random_num(num_len):
    """
    获取随机整形数
    :param num_len: 长度
    :return:
    """
    str_list = NUM[int(random.uniform(1, len(NUM)))]

    for i in range(1, num_len):
        str_list = str_list + NUM[int(random.uniform(0, len(NUM)))]
        pass
    return int(str_list)


def get_random_str(str_len):
    """
    获取随机字符串
    :param str_len: 需要获取的长度
    :return:
    """
    str_list = ""
    for i in range(0, str_len):
        str_list = str_list + STR[int(random.uniform(0, len(STR)))]
        pass
    return str_list
    pass


def remove_duplicate(list):
    """
    去掉列表中的重复数据
    :param list:
    :return:
    """
    temp = {}
    for item in list:
        temp[item] = ""
        pass
    return temp.keys()
    pass


def get_duplicate(list):
    """
    获取列表中的重复数据
    :param list:
    :return:
    """
    temp = {}
    temp_list = []
    for item in list:
        flag = temp.has_key(item)
        temp[item] = ""
        if flag is True:
            temp_list.append(item)
        pass
    return remove_duplicate(temp_list)
    pass


def upper_first_char_case(str):
    """
    首字母大写
    :param str:
    :return:
    """
    if str is None or str is "":
        return str

    first_char = str[0]
    if ord('a') < ord(first_char) < ord('z'):
        return "%s%s" % (chr(ord(first_char) - 32), str[1:len(str)])
    return str


def lower_first_char_case(str):
    """
    首字母小写
    :param str:
    :return:
    """
    if str is None or str is "":
        return str

    first_char = str[0]
    if ord('A') < ord(first_char) < ord('Z'):
        return "%s%s" % (chr(ord(first_char) + 32), str[1:len(str)])
    return str


def get_nums_from_str(str):
    """
    获取字符串中的数字
    :param str:
    :return:
    """
    nums = []
    ser = re.search(r'\d+', str)

    while ser:
        num = ser.group()
        nums.append(int(num))
        str = str[str.index(num) + len(num):len(str)]
        ser = re.search(r'\d+', str)
    return nums
    pass


def check_sensitive(str, sens):
    """
    检查字符串中是否有敏感词
    :param str:
    :param sens:
    :return:
    """
    for sen in sens:
        if sen in str:
            return True
    return False


def md5(str):
    """
    计算字符的md5摘要
    :param str:
    :return:
    """
    return hashlib.md5(str).hexdigest()


def sha1(str):
    """
    计算字符的sha1炸药
    :param str:
    :return:
    """
    return hashlib.sha1(str).hexdigest()


def create_short_url(url):
    """
    生成短连接
    :param url:
    :return:
    """
    secert = md5(md5("create_short_url") + url).upper()
    total_arr = []
    for i in range(0, 4):
        # 把加密字符按照 8 位一组 16 进制与 0x3FFFFFFF 进行位与运算
        temp = secert[i * 8:i * 8 + 8]
        hex_long = 0x3FFFFFFF & int(temp, 16)

        temp_arr = []
        for j in range(0, 6):
            # 把得到的值与 0x0000003D 进行位与运算，取得字符数组 chars 索引
            index = 0x0000003D & hex_long
            temp_arr.append(CHARS[index])
            # 每次循环按位右移 5 位
            hex_long >>= 5
            pass
        total_arr.append(temp_arr)

    # 在数组中随机一组字符作为短连接
    return ''.join(total_arr[int(random.uniform(0, 4))])
    pass


# def create_qrcode(str, save_path):
#     """
#     生成二维码
#     :param str:
#     :param save_path:
#     :return:
#     """
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(str)
#     qr.make(fit=True)
#
#     img = qr.make_image()
#     img.save(save_path)
#     img.show()


def filter_json(json, **params):
    '''
    过滤json数据
    :param json:
    :param params:
    :param source_include:
    :return:
    '''
    source_include = None
    if 'source_include' in params:
        source_include = params['source_include']
    source_exclude = None
    if 'source_exclude' in params:
        source_exclude = params['source_exclude']

    temp = {}
    if source_include:
        for item in source_include:
            temp[item] = json[item]
        return temp
    elif source_exclude:
        for item in source_exclude:
            del json[item]
        return json


def make_timestamp(str_time, format_str):
    return int(time.mktime(time.strptime(str_time, format_str)))


def make_timestamp_for_sql_time(str_time):
    return make_timestamp(str_time, BaseConfig.TIMESTAMP_FORMAT_SQL)


def map_model_item(item):
    """map lambda方法 格式化item"""
    item = format_model_item(item)


def format_model_item(item):
    ext = item.get('ext', '{}')
    if not ext:
        ext = '{}'
    item['ext'] = json.loads(ext)

    banner = item.get('banner')
    if banner:
        item['banner'] = json.loads(banner)

    last_upload = item.get('last_upload')
    if last_upload:
        item['last_upload'] = json.loads(last_upload)
    posters = item.get('posters', None)
    if posters:
        item['posters'] = json.loads(posters)
    return item


def test_utils():
    return True


if __name__ == '__main__':
    # list = [1, 2, 3, 4, 5, 5, 5, 4, 4, 5, 6, 7, 8, 7, 6,10]
    # url = "https://1lybcxulxb.execute-api.us-west-2.amazonaws.com/production/v1/hotWords"
    # key = "name"

    json = {
        "_id": "58cd320f1ac463f48938d945",
        "index": 0,
        "picture": "http://placehold.it/32x32",
        "eyeColor": "green",
        "name": {
            "first": "Jones",
            "last": "Crosby"
        },
        "company": "CALCULA",
        "friends": [
            {
                "id": 0,
                "name": "Amy Kim"
            },
            {
                "id": 1,
                "name": "Small Fields"
            }
        ]
    }

    filter_json(json, source_include='balance')

    # str = os.popen("cd /data/temp && ls").read()
    # a = str.split("\n")
    # for b in a:
    #     print b
    pass
