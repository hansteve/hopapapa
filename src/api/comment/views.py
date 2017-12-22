#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''评论表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.api.comment import models as comt_db
from src.api.comment.models import Comment
from src.api.comment.service import get_comments
from src.common.http_util import check_params
from src.common.http_util import return_not_found
from src.common.http_util import return_no_authorization
from src.common.http_util import get_login_user_id
from src.common import http_util
from src.common.web.flask_snippets import jsonp
from src.config import BaseConfig

from flask import request
from flask import Blueprint

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/comment/create', methods=['POST'])
def create_comment():
    '''评论'''
    args = request.json
    key = check_params(args, 'res_id', 'content')
    if key:
        return return_not_found(key)

    # 获取用户id
    user_id = get_login_user_id(request)
    if not user_id:
        return return_no_authorization()

    res_id = args['res_id']
    content = args['content']

    comt_db.create_comment(user_id=user_id, res_id=res_id, content=content)

    return http_util.return_model()


@comment_bp.route('/reply/create', methods=['POST'])
def create_reply():
    '''回复'''
    args = request.json
    key = check_params(args, 'to_user_id', 'comment_id', 'content')
    if key:
        return return_not_found(key)

    # 获取用户id
    user_id = get_login_user_id(request)
    if not user_id:
        return return_no_authorization()

    to_user_id = args['to_user_id']
    comment_id = args['comment_id']
    content = args['content']

    comt_db.create_reply(
        user_id=user_id,
        to_user_id=to_user_id,
        comment_id=comment_id,
        content=content
    )

    return http_util.return_model()


@comment_bp.route('/comment', methods=['GET'])
@jsonp
def comments():
    '''评论列表'''
    args = request.args
    key = check_params(args, 'res_id')
    if key:
        return return_not_found(key)

    start = http_util.get_param_int(args, 'start', BaseConfig.MAX_START)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_NO_PAGINATE_PER_PAGE)

    res = get_comments(
        res_id=args['res_id'],
        start=start,
        per_page=per_page
    )

    return http_util.return_model(res)
