#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''location表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.common import aws_es as es
from src.common.web.flask_snippets import args_required
from src.api.user.service import get_user_attention_status
from src.api.home_page.models import ViewHotRes
from src.api.home_page.service import Resource

from flask import Blueprint
from flask import g
from flask import request

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
@args_required('q')
def search():
    '''搜索'''
    args = request.args
    user_id = g.user_id
    q = args.get('q')
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)
    q = 'name:{}'.format(q)

    doc_type = "{},{},{},{},{}".format(
        BaseConfig.ES_TYPE_USER, BaseConfig.ES_TYPE_ARTICLE,
        BaseConfig.ES_TYPE_COLLECTION, BaseConfig.ES_TYPE_VIDEO,
        BaseConfig.ES_TYPE_AUDIO
    )

    res, total = es.search(
        index=BaseConfig.ES_INDEX,
        doc_type=doc_type,
        q=q,
        sort='{}:desc'.format(BaseConfig.ES_PARAMS_WEIGHT),
        _source_include=['res_id', 'res_type', 'name', 'portrait', 'poster',
                         'posters', 'age']
    )

    for item in res:
        res_type = item['res_type']
        res_id = item['res_id']
        if res_type == BaseConfig.TYPE_USER:
            item['attention_status'] = get_user_attention_status(user_id,
                                                                 res_id)

    res = http_util.make_page_response(res, total, page, per_page)

    if not res['items']:
        res['recommends'] = Resource.get_hot_items()

    return http_util.return_model(res)


@search_bp.route('/search/key', methods=['GET'])
@args_required('q')
def search_key():
    '''搜索'''
    args = request.args
    q = args.get('q')
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)
    q = 'name:{}'.format(q)

    doc_type = "{},{},{},{},{}".format(
        BaseConfig.ES_TYPE_USER, BaseConfig.ES_TYPE_ARTICLE,
        BaseConfig.ES_TYPE_COLLECTION, BaseConfig.ES_TYPE_VIDEO,
        BaseConfig.ES_TYPE_AUDIO
    )

    res, total = es.search(
        index=BaseConfig.ES_INDEX,
        doc_type=doc_type,
        q=q,
        sort='{}:desc'.format(BaseConfig.ES_PARAMS_WEIGHT),
        _source_include=['name']
    )

    res = http_util.make_page_response(res, total, page, per_page)

    return http_util.return_model(res)
