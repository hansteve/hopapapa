#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''网易云服务'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import requests

from src import app
from src.config import BaseConfig
from src.common.wangyi.ServerAPI import ServerAPI

AppKey = BaseConfig.WANGYI_APP_KEY
AppSecret = BaseConfig.WANGYI_APP_SECRET

api = ServerAPI(AppKey, AppSecret)


def post(url, data):
    '''网银云post请求'''
    api.checkSumBuilder()
    res = requests.post(
        url=url,
        headers={
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "AppKey": api.AppKey,
            "CurTime": "{}".format(api.CurTime),
            "CheckSum": "{}".format(api.CheckSum),
            "Nonce": "{}".format(api.Nonce),
        },
        data=data
    )

    data = res.json()
    if data['code'] != 200:
        app.logger.debug("wangyi send code error {}".format(data))
    return res
