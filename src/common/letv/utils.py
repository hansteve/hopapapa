#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''letv工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time
import hashlib
import requests

from src import app
from src.config import BaseConfig


def post(url, api, params=None):
    data = {
        'timestamp': int(time.time()),
        'user_unique': BaseConfig.LETV_USER_UNIQUE,
        'api': api,
        'format': 'json',
        'ver': '2.0'
    }

    if params:
        for key, value in params.iteritems():
            data[key] = value

    sign_str = ''
    for k, v in sorted(data.items(), key=lambda x: x[0], reverse=False):
        sign_str = sign_str + k + '{}'.format(v) + ''
    sign_str = sign_str + BaseConfig.LETV_KEY_SECRET

    sign = md5(sign_str)
    data['sign'] = sign

    res = requests.post(
        url=url,
        data=data
    )

    res = res.json()

    code = res['code']

    if code != 0:
        app.logger.error(res['message'])

    return res['data']


def md5(str):
    """
    计算字符的md5摘要
    :param str:
    :return:
    """
    return hashlib.md5(str).hexdigest()
