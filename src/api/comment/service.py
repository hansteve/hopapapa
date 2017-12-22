#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''评论表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.config import BaseConfig
from src.api.comment.models import Comment
from src.api.user.service import get_user_detail


def get_comments(res_id, start, per_page):
    comments = Comment.get_comments(
        res_id=res_id,
        start=start,
        per_page=per_page
    )

    map(loop_comments, comments)

    return comments


def get_replys(comment_id):
    replys = Comment.get_replys(comment_id=comment_id)
    map(loop_comments, replys)
    return replys


def loop_comments(item):
    '''制作评论列表'''
    # 构造用户信息
    user_id = item['user_id']
    item['from_user'] = get_user_detail(
        id=user_id,
        source_exclude=['age', 'gender', 'mobile', 'create_ts', 'ext']
    )

    # 构造回复
    res_type = item['res_type']
    comment_id = item['comment_id']
    if res_type == BaseConfig.TYPE_RES:
        replys = get_replys(comment_id)
        if replys:
            item['replys'] = replys
    elif res_type == BaseConfig.TYPE_COMMENT:
        del item['comment_id']

        to_user_id = item['to_user_id']
        to_user = get_user_detail(
            id=to_user_id,
            source_exclude=['age', 'gender', 'mobile', 'create_ts', 'ext']
        )
        item['to_user'] = to_user

    del item['res_type']
    del item['to_user_id']
    del item['user_id']
