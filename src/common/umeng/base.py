#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''aliyun工具类'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import hashlib
import json
import time
import requests

from src import env_config
from src.config import BaseConfig


class UmengBase(object):
    API_PUSH_URL = 'https://msgapi.umeng.com/api/send'

    def __init__(self, key=BaseConfig.UMENG_KEY,
                 secret=BaseConfig.UMENG_SECRET):
        self.key = key
        self.secret = secret

    def make_sign(self, params, url=API_PUSH_URL, method='POST'):
        post_body = json.dumps(params)
        return md5('%s%s%s%s' % (method, url, post_body, self.secret))

    def call_push(self, type, alert, device_token=None, source='ios',
                  custom_params=None):
        payload = {
            "aps": {"alert": alert}
        }

        if custom_params:
            for key,value in custom_params.iteritems():
                payload[key] = value

        params = {'appkey': self.key,
                  'timestamp': int(time.time()),
                  'device_tokens': device_token,
                  'type': type,
                  'payload': payload,
                  'production_mode': env_config.UMENG_PRODUCTION_MODE
                  }
        sign = self.make_sign(params)

        url = '{}?sign={}'.format(UmengBase.API_PUSH_URL, sign)

        res = requests.post(
            url=url,
            json=params
        )
        return Response(res)


def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()


class Response:
    def __init__(self, response):
        self.response = response

    @property
    def result(self):
        """调用结果"""
        return self.response.json()

    @property
    def status(self):
        """Http 返回码"""
        return self.response.status_code

    @property
    def ok(self):
        """调用成功返回True，其它返回False"""
        return self.response.ok

    def get(self):
        """返回调用结果"""
        return self.result

    def __str__(self):
        """打印字符串"""
        return str(self.result)


