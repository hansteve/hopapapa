#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''短信业务'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import requests

from src.common.wangyi import server
from src import app


def send_code(mobile, templateid):
    '''发送短信验证码'''
    res = server.post(
        url='https://api.netease.im/sms/sendcode.action',
        data={
            "mobile": mobile,
            "templateid": templateid
        }
    )
    data = res.json()
    status_code = data['code']
    if status_code == 200:
        return data['obj']
    else:
        return None


def verify_code(mobile, code):
    '''发送短信验证码'''

    res = server.post(
        url='https://api.netease.im/sms/verifycode.action',
        data={
            "mobile": mobile,
            "code": code
        }
    )
    data = res.json()
    status_code = data['code']
    if status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    # http://59.110.168.49:8000/api/v1/code/send
    # http://59.110.168.49:8000/api/v1/user/create/anonymous
    # http://59.110.168.49:8000/api/v1/user/detail

    res = requests.post(
        url='http://59.110.168.49:8000/api/v1/code/send',
        json={"mobile": "18311233541"}
    )

    res = requests.get(
        url='http://59.110.168.49:8000/api/v1/user/detail',
        headers={
            "authorization": "NTY5NDIxNjA1NTM7MTQ5MDIwMzM5Ng=="
        }
    )

    # curl - X
    # POST - H
    # "AppKey: go9dnk49bkd9jd9vmel1kglw0803mgq3" - H
    # "CurTime: 1443592222" - H
    # "CheckSum: 9e9db3b6c9abb2e1962cf3e6f7316fcc55583f86" - H
    # "Nonce: 4tgggergigwow323t23t" - H
    # "Content-Type: application/x-www-form-urlencoded" - d
    # 'mobile=13812345678' 'https://api.netease.im/sms/sendcode.action'


    # code = send_code(
    #     mobile="18311233541",
    #     templateid="3061150"
    # )
    # print(code)

    is_exist = verify_code(
        mobile="18311233541",
        code="2814"
    )
    print(is_exist)
