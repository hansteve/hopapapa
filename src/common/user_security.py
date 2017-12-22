#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户加密'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import base64
import time

from src import app


class UserSecurity():
    @classmethod
    def generate_authorization(cls, user_id, **params):
        '''用户id加密'''
        data = '{};{}'.format(user_id, int(time.time()))
        return base64.b64encode(data)

    @classmethod
    def get_user_id(cls, authorization):
        '''从加密信息中过去用户'''
        try:
            if not authorization or authorization == 'null':
                return None
            data = base64.b64decode(authorization)
            return data.split(';')[0]
        except BaseException as e:
            app.logger.error(e)
            return None


def generate_authorization(user_id, **params):
    '''用户id加密'''
    data = '{};{}'.format(user_id, int(time.time()))
    return base64.b64encode(data)


def get_user_id(authorization):
    '''从加密信息中过去用户'''
    try:
        if not authorization or authorization == 'null':
            return None
        data = base64.b64decode(authorization)
        return data.split(';')[0]
    except BaseException as e:
        app.logger.error(e)
        return None
