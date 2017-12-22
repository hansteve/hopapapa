#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户表models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common.user_security import generate_authorization
from src.common.user_security import get_user_id


def test_get_user_id():
    authorization = 'sfawefasdfawef'
    user_id = get_user_id(authorization)
    assert user_id == None

    authorization = 'MTEyNTM0NjAxMTQ7MTQ4OTUwOTkwNA=='

    assert get_user_id(authorization) == 11253460114


def test_generate_authorization():
    user_id = 11253460114
    authorization = generate_authorization(user_id)
    assert user_id == get_user_id(authorization)
