#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户表service'''
from elasticsearch.client import query_params

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.config import BaseConfig
from src.api.user.models import UserAttention
from src.api.user.models import User
from src.api.user.models import UserOpen
from src.api.video.models import Video
from src.api.action.models import Action
from src.api.location.models import Location
from src.common import http_util
from src.common import utils

from flask import g


@query_params('login_user_id')
def get_user_attentions(user_id, attention_status, page, per_page, params=None):
    """获取用户关注或者被关注列表"""
    paginate = None
    users = []
    total = 0
    login_user_id = params.get('login_user_id')
    if attention_status == BaseConfig.TYPE_ATTENTION_STATUS_LIST:
        paginate = UserAttention.query_user_attention_paginate(
            user_id=user_id,
            page=page,
            per_page=per_page
        )

        if paginate:
            items = paginate.items
            for item in items:
                user_detail = get_user_detail(
                    id=item.to_user_id,
                    login_user_id=login_user_id,
                    source_include=['view_count']
                )
                users.append(user_detail)

            total = paginate.total

    elif attention_status == BaseConfig.TYPE_ATTENTION_STATUS_BY_LIST:
        paginate = UserAttention.query_user_attention_paginate(
            to_user_id=user_id,
            page=page,
            per_page=per_page
        )

        if paginate:
            items = paginate.items
            for item in items:
                user_detail = get_user_detail(
                    id=item.user_id,
                    login_user_id=login_user_id,
                    source_include=['view_count']
                )
                users.append(user_detail)

            total = paginate.total

    res = http_util.make_page_response(users, total, page,
                                       per_page)

    return res


@query_params('login_user_id')
def get_user_detail(id, source_include=[], source_exclude=[], params=None):
    """获取用户详情"""
    user = User.query_user(id=id)

    item = User.get_detail(id)

    # 查找第三方用户
    if 'opens' in source_include:
        opens = []
        for open_user in user.opens:
            opens.append({
                "open_id": open_user.id,
                "source": open_user.source
            })
        item['opens'] = opens

    login_user_id = params.get('login_user_id', None)
    if login_user_id:
        # 拼装关注状态
        attention_status = get_user_attention_status(login_user_id, id)

        item['attention_status'] = attention_status

    # 观看数量
    if 'view_count' in source_include:
        views = Action.query_user_views(id)
        item['ext']['view_count'] = len(views)
    # 关注数
    if 'attention_count' in source_include:
        attens = UserAttention.query_user_attentions(to_user_id=id)
        item['ext']['attention_count'] = len(attens)

    # 获取最后一次地理位置
    item['ext']['last_location_time'] = Location.get_user_last_location_time(id)

    if source_exclude:
        for field in source_exclude:
            del item[field]
    return item


def get_user_attention_status(user_id, to_user_id):
    """获取关注状态"""

    attention_status = BaseConfig.TYPE_ATTENTION_STATUS_NO
    if not user_id:
        return attention_status
    ua = UserAttention.query_user_attention(
        user_id=user_id,
        to_user_id=to_user_id
    )
    if ua:
        attention_status = BaseConfig.TYPE_ATTENTION_STATUS_YES
        oua = UserAttention.query_user_attention(
            user_id=to_user_id,
            to_user_id=user_id
        )
        if oua:
            attention_status = BaseConfig.TYPE_ATTENTION_STATUS_EACH_OTHER
    return attention_status


def delete_user_by_id(user_id):
    """删除用户"""
    user = User.query_user(
        id=user_id
    )

    if user:
        User.update_user_by_id(
            id=user_id,
            is_del=1
        )

        # 检查是否为第三方用户
        uos = UserOpen.query_items(
            user_id=user_id
        )
        print(len(uos))
        if uos:
            for uo in uos:
                UserOpen.update_open_user_by_id(
                    id=uo.id,
                    user_id=""
                )
        return True
    return False


def get_similar_users(user_id):
    items = []
    for item in User.get_similar_users(user_id):
        user_id = None
        if g.user:
            user_id = g.user.id
        item['attention_status'] = get_user_attention_status(user_id,
                                                             item['user_id'])
        items.append(item)
    return items  # list(map(map_user, User.get_similar_users(user_id)))


def map_user(item):
    user_id = None
    if g.user:
        user_id = g.user.id
    item['attention_status'] = get_user_attention_status(user_id,
                                                         item['user_id'])
