#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''首页views'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys

from src import app
from src.config import BaseConfig
from src.common import http_util
from src.api.home_page.models import HomePage
from src.api.home_page.models import ViewHotRes
from src.api.home_page.service import Resource
from src.api.action.models import Action
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint
from flask import g

reload(sys)
sys.setdefaultencoding('utf8')

home_page_bp = Blueprint('home_page', __name__)


@home_page_bp.route('/home_page/<int:type>', methods=['GET'])
@jsonp
def home_page(type):
    '''
    :param type: 83:首页  87:热门内容
    :return:
    '''
    args = request.args
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)
    login_user_id = g.user_id
    res = None
    if type == BaseConfig.TYPE_HOME_PAGE:
        # 首页列表
        paginate = Resource.get_home_page_paginate(
            type=BaseConfig.TYPE_HOME_PAGE_LIST,
            page=page,
            per_page=per_page
        )
        res = http_util.make_page_response(paginate.items, paginate.total, page,
                                           per_page)
        # 轮播图
        paginate = Resource.get_home_page_paginate(
            type=BaseConfig.TYPE_HOME_PAGE_CAROUSEL,
            page=page,
            per_page=per_page
        )
        carousels = paginate.items
        res['carousels'] = carousels
        # 静态地址
        res['url'] = ""
        hp_url = HomePage.query_home_page(
            type=BaseConfig.TYPE_HOME_PAGE_URL
        )
        if hp_url:
            res['url'] = hp_url.url
        # 弹窗
        res['show_resource'] = Resource.get_show_resource(login_user_id)
        # 推荐
        paginate = Resource.get_home_page_paginate(
            type=BaseConfig.TYPE_HOME_PAGE_RECOMMEND,
            page=page,
            per_page=per_page
        )
        res['recommends'] = paginate.items

    elif type == BaseConfig.TYPE_HOME_PAGE_HOT:
        res = get_hot_res()
        if page >1:
            res['items'] = []

    return http_util.return_model(
        data=res
    )


def get_hot_res():
    recommends = HomePage.query_home_pages(
        type=BaseConfig.TYPE_HOME_PAGE_HOT,
        is_online=1
    )
    hot_res = ViewHotRes.query_items()
    print(len(recommends), len(hot_res))

    hot_res = hot_res[0:10]

    items = recommends + hot_res

    items = Resource.format_items(items)

    recommends = items[0:4]

    res = http_util.make_page_response(items[4:], len(items[4:]), 1,
                                       len(items[4:]))

    res['recommends'] = recommends

    return res


@home_page_bp.route('/resource/detail', methods=['GET'])
@jsonp
def resource_detail():
    """资源详情"""
    args = request.args
    key = http_util.check_params(args, 'res_id', 'res_type')
    if key:
        return http_util.return_param_not_found(key)

    login_user_id = http_util.get_login_user_id(request)

    res_id = http_util.get_param(args, 'res_id')
    res_type = http_util.get_param_int(args, 'res_type')

    try:
        detail = Resource.get_resource_detail(
            res_id=res_id,
            res_type=res_type,
            source_include=['comments', 'related_items', 'view_count',
                            'like_count', 'items',
                            'comment_count'],
            login_user_id=login_user_id
        )

        if not detail:
            return http_util.return_404('res_id not found')

        # 记录用户行为
        Action.create_action(
            user_id=login_user_id,
            type=BaseConfig.TYPE_ACTION_VIEW,
            res_id=res_id,
            res_type=res_type
        )

        return http_util.return_model(
            data=detail
        )
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@home_page_bp.route('/resource/delete', methods=['POST'])
def resource_delete():
    """资源详情"""
    args = request.json
    key = http_util.check_params(args, 'res_id', 'res_type')
    if key:
        return http_util.return_param_not_found(key)

    login_user_id = http_util.get_login_user_id(request)

    if not login_user_id:
        return http_util.return_no_authorization()

    res_id = http_util.get_param(args, 'res_id')
    res_type = http_util.get_param_int(args, 'res_type')

    try:
        is_del = Resource.delete_resource(res_id, res_type)

        if not is_del:
            return http_util.return_internal_server_error("删除失败")

        # 记录用户行为
        Action.create_action(
            user_id=login_user_id,
            type=BaseConfig.TYPE_ACTION_DELETE,
            res_id=res_id,
            res_type=res_type
        )

        return http_util.return_model()
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@home_page_bp.route('/launch', methods=['GET'])
@jsonp
def launch():
    """启动接口"""
    try:
        res = {}
        #
        # hp = HomePage.query_daily_resource()
        #
        # if hp:
        #     hp_show = Resource.get_resource_detail(hp.res_id, hp.res_type)
        #     if hp_show:
        #         res['home_page_show_resource'] = hp_show

        res['map_urls'] = [
            'http://img.hopapapa.com/common/13207_3550',
            'http://img.hopapapa.com/common/13208_3550',
        ]



        return http_util.return_model(res)
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()
