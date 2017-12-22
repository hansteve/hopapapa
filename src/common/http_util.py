#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''base工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time

from src.config import BaseConfig
from src.common.user_security import get_user_id

from flask import make_response
from flask import jsonify
from flask import request


def return_model(data=None, status=200, message=None, header=None):
    """
    api返回数据model
    :param data: 默认使用空json
    :param status: 接口状态码，可以影响head返回的status code
    :param message: 接口错误时，返回的信息
    :return:
    """
    if not message:
        message = 'success'
    res = {
        "status": status,
        "message": message,
        "version": int(time.time())
    }
    if data:
        res['data'] = data
    return make_response(jsonify(res), status, header)


def return_page(data, total, page, per_page):
    res = make_page_response(data, total, page, per_page)
    return return_model(
        data=res
    )


def return_not_found(key):
    return return_param_not_found(key)


def return_param_not_found(key):
    '''返回找不到参数的结果'''
    return return_model(
        message='param {} not found'.format(key),
        status=400
    )


def return_no_authorization():
    '''检查用户身份失败'''
    return return_model(
        message='authorization check failed',
        status=401
    )


def return_forbidden(message='Forbidden'):
    '''拒绝请求'''
    return return_model(
        message=message,
        status=403
    )


def return_404(message='resource is not found'):
    '''资源找不到'''
    return return_model(
        message=message,
        status=404
    )


def return_internal_server_error(message='Internal Server Error'):
    '''服务器错误'''
    return return_model(
        message=message,
        status=500
    )


def check_params(params, *keys):
    '''查找参数'''
    if not params:
        return keys[0]
    for key in keys:
        if key not in params:
            return key

    return None


def get_login_user_id(request):
    '''从request中过去user_id'''
    headers = request.headers

    callback = request.args.get('callback', False)
    if callback:
        headers = request.cookies

    key = check_params(headers, BaseConfig.HEAD_AUTHORIZATION)
    if key:
        return None

    token = headers[BaseConfig.HEAD_AUTHORIZATION]
    # 获取用户id
    return get_user_id(token)


def get_param(params, key, default=None):
    '''获取参数'''
    if key in params:
        return params[key]
    else:
        return default


def get_param_int(params, key, default=0):
    '''获取参数'''
    value = get_param(params, key, default)
    if value:
        return int(value)
    return None


def make_page_response(data, total_size, page, size):
    """
    生成返回数据
    :param list:
    :param total_size:
    :param page:
    :param size:
    :return:
    """
    total_page = total_size / size
    yu = total_size % size
    if yu > 0:
        total_page += 1

    print(total_page)
    res = {
        "items": data,
        "cur_page": int(page),
        "total_items": total_size,
        "total_pages": total_page,
        "item_per_page": size
    }
    return res


def get_params_from_request(key, default):
    print(request.method)
    method = request.method

    params = {}
    if method == 'GET':
        params = request.args
    else:
        content_type = request.content_type
        if content_type == 'application/json':
            params = request.json
        else:
            params = request.form
