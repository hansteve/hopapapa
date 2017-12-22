#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户表models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common.rongcloud.client import User
from src.common.rongcloud.base import RongCloudBase




if __name__ == '__main__':
    # print(User._app_key)
    u = User()
    res = u.getToken(userId='userid1', name='username', portraitUri='http://www.rongcloud.cn/images/logo.png')
    print(type(res))
    print(res.result['token'])

    # r = RongCloudBase.call_api(
    #     method=('API', 'POST', 'application/x-www-form-urlencoded'),
    #     action='/user/getToken.json',
    #     params={
    #         "userId": 1,
    #         "name": "1",
    #         "portraitUri": ""
    #     })

    print(res)