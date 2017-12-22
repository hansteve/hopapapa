#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''like表views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.api.like.models import LikeInfo
from src.common.http_util import return_404
from src.common import http_util
from src.common.web.flask_snippets import login_required
from src.common.web.flask_snippets import args_required

from flask import request
from flask import Blueprint
from flask import g

like_bp = Blueprint('like', __name__)


@like_bp.route('/like/<string:action>', methods=['POST'])
@login_required
@args_required('res_id', 'res_type')
def like(action):
    '''
    点赞取消点赞
    :param action: on:点赞、off:取消
    :user_id
    :to_id
    :to_id_type
    :return:
    '''
    args = request.json
    user_id = g.user_id

    res_id = args.get('res_id')
    if not res_id:
        return http_util.return_forbidden('res_id can not be empty')
    res_type = args['res_type']

    if action == 'on':
        LikeInfo.dis_like(
            user_id=user_id,
            res_id=res_id,
            res_type=res_type
        )
        LikeInfo.create_like(
            user_id=user_id,
            res_id=res_id,
            res_type=res_type
        )
    elif action == 'off':
        LikeInfo.dis_like(
            user_id=user_id,
            res_id=res_id,
            res_type=res_type
        )
    else:
        return return_404()

    return http_util.return_model()
