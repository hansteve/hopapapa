#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''user views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.user.models import User
from src.api.user.service import delete_user_by_id
from src.common.http_util import return_model
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_user_bp = Blueprint('admin_user', __name__)


@admin_user_bp.route('/user/list.json', methods=['GET'])
@jsonp
def list():
    '''首页列表'''
    args = request.args
    type = http_util.get_param_int(args, 'type', BaseConfig.TYPE_HOME_PAGE_LIST)
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = User.query_paginate(
        page=page,
        status=BaseConfig.TYPE_USER_NORMAL,
        per_page=per_page
    )

    details = []
    for item in paginate.items:
        detail = item.to_json()
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_user_bp.route('/user/delete.json', methods=['POST'])
def delete():
    '''首页列表'''
    args = request.form
    id = args.get('id', None)
    if id:
        flag = delete_user_by_id(id)
        if flag:
            return http_util.return_model()
        else:
            return http_util.return_internal_server_error()
    else:
        return http_util.return_forbidden('id not found')
