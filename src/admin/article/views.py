#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''article表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.article import models
from src.api.article.models import Article
from src.common.http_util import check_params
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_article_bp = Blueprint('admin_acticle', __name__)


@admin_article_bp.route('/article/create', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def create_article():
    '''创建文章'''
    print(request.form)
    print(request.content_type)
    args = request.form
    key = check_params(args, 'name', 'content')
    if key:
        return http_util.return_param_not_found(key)

    a = Article.create_article(**args)

    return return_model(
        data={
            "article_id": a.id
        }
    )


@admin_article_bp.route('/article/list.json', methods=['GET'])
@jsonp
def get_article_list_json():
    '''获取文章内容'''
    args = request.args
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = Article.query_article_paginate(
        page=page,
        per_page=per_page
    )
    details = []
    for item in paginate.items:
        detail = item.to_json()
        del detail['content']
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_article_bp.route('/article/edit.json', methods=['POST'])
def get_article_edit_json():
    '''获取文章内容'''
    args = request.form

    id = args.get('id', None)

    if id:
        Article.update_article_by_id(**args)

    return return_model()
