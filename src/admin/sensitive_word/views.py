#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''sunsitive word views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.sensitive_word.models import SensitiveWord
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_sensitive_word_bp = Blueprint('admin_sensitive_word', __name__)


@admin_sensitive_word_bp.route('/sensitive_word/list.json', methods=['GET'])
@jsonp
def list():
    '''文章列表'''

    args = request.args

    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = SensitiveWord.query_paginate(
        page=page,
        per_page=per_page
    )

    items = []
    for item in paginate.items:
        detail = item.to_json()
        # detail['id'] = "{}".format(detail['id'])
        items.append(detail)

    res = http_util.make_page_response(items, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_sensitive_word_bp.route('/sensitive_word/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def edit():
    '''创建文章'''
    args = request.form
    id = args.get('id', None)

    if id:
        SensitiveWord.update_by_id(**args)
    else:
        SensitiveWord.create(**args)

    return return_model()


@admin_sensitive_word_bp.route('/sensitive_word/delete.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def delete():
    '''删除敏感词'''
    args = request.form
    id = args.get('id', None)

    SensitiveWord.update_by_id(
        id=id,
        is_del=1
    )


    return return_model()
