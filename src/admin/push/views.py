#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''push view'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.config import BaseConfig
from src.api.push.models import Push
from src.common import http_util
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp
from src.common.umeng.client import UmengPush

umeng_push = UmengPush()

from flask import request
from flask import Blueprint

admin_push_bp = Blueprint('admin_push', __name__)


@admin_push_bp.route('/push.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def push_msg():
    args = request.form

    res = umeng_push.push_ios_all(
        alert=args['description'],
        custom_params=args
    )
    print(res.result)

    if res.ok:
        p = Push.create_push(**args)
        if p:
            return http_util.return_model()

    return http_util.return_internal_server_error()


@admin_push_bp.route('/push/list.json', methods=['GET'])
@jsonp
def push_list():
    args = request.args
    page = http_util.get_param_int(args, "page", BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, "per_page",
                                       BaseConfig.DEFAULT_PER_PAGE)

    print(page, per_page)

    paginate = Push.query_paginate(page, per_page)

    details = []
    for item in paginate.items:
        detail = item.to_json()
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return http_util.return_model(
        data=res
    )
