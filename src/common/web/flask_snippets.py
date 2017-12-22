#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''flask支持片段代码'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from datetime import timedelta
from functools import update_wrapper
from functools import wraps
from flask import make_response
from flask import request
from flask import current_app
from flask import g
from src.common import http_util


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    Decorator for the HTTP Access Control
    :param origin:
    :param methods:
    :param headers:
    :param max_age:
    :param attach_to_all:
    :param automatic_options:
    :url    http://flask.pocoo.org/snippets/56/
    :return:
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


def jsonp(func):
    """
    Wraps JSONified output for JSONP requests.
    :param func:
    :URL    http://flask.pocoo.org/snippets/79/
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function

def args_required(*params):
    """
    检查参数
    """

    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            content_type = request.content_type
            _args = None
            if content_type == 'application/x-www-form-urlencoded':
                _args = request.form
            elif content_type == 'application/json':
                _args = request.json
            else:
                _args = request.args

            for param in params:
                if param not in _args:
                    return http_util.return_forbidden(
                        '{} is necessary'.format(param))
            return func(*args, **kwargs)

        return _wrapped

    return _wrapper

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return http_util.return_no_authorization()
        return f(*args, **kwargs)

    return decorated_function
