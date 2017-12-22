#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.home_page.models import HomePage
from src.api.home_page.service import Resource
from src.api.video.models import Video
from src.api.video.service import get_videos
from src.api.article.service import get_articles
from src.api.article.models import Article
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_home_page_bp = Blueprint('admin_home_page', __name__)


@admin_home_page_bp.route('/home_page/list.json', methods=['GET'])
@jsonp
def list():
    '''首页列表'''
    args = request.args
    type = http_util.get_param_int(args, 'type', BaseConfig.TYPE_HOME_PAGE_LIST)
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = HomePage.query_home_page_paginate(
        type=type,
        page=page,
        per_page=per_page
    )

    details = []
    for item in paginate.items:
        detail = item.to_json()
        res_type = detail['res_type']
        res_id = detail['res_id']
        res_detail = Resource.get_resource_detail(
            res_id=res_id,
            res_type=res_type
        )
        detail['res_detail'] = res_detail
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_home_page_bp.route('/resource/list.json', methods=['GET'])
@jsonp
def resource_list():
    '''首页列表'''
    args = request.args
    res_type = http_util.get_param_int(args, 'res_type', 7)

    res = Resource.get_resource_list(res_type)

    return return_model(
        data=res
    )


@admin_home_page_bp.route('/resource/delete.json', methods=['POST'])
def resource_delete_json():
    '''首页列表'''
    args = request.form

    res_id = http_util.get_param(args, 'res_id', None)
    res_type = http_util.get_param_int(args, 'res_type', 0)

    if not res_id or not res_type:
        return http_util.return_forbidden('res_id or res_type is error')

    check_use = Resource.check_resource_use_status(res_id, res_type)
    if check_use:
        return http_util.return_forbidden("{}，不能删除".format(check_use))

    res = Resource.delete_resource(res_id, res_type)

    if res:
        return return_model()
    else:
        return http_util.return_internal_server_error()


@admin_home_page_bp.route('/home_page/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def edit_json():
    """创建或修改首页信息"""
    args = request.form
    id = args.get('id', None)

    if id:
        res = HomePage.update_home_page_by_id(**args)
        print(res.to_json())
    else:
        HomePage.create_home_page(**args)

    return return_model()


@admin_home_page_bp.route('/home_page/delete.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def delete_json():
    """创建或修改首页信息"""
    args = request.form
    id = args.get('id', None)

    hp = None
    if id:
        hp = HomePage.update_home_page_by_id(
            id=id,
            is_del=1
        )

    if hp:
        return http_util.return_model()
    else:
        return http_util.return_forbidden()
