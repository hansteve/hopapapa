#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''视频逻辑模块'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys

from src.api.user.models import User
from src.api.video.models import Video
from src.api.action.models import Action
from src.common import http_util
from src.common.letv import video_client
from src.common.web.flask_snippets import jsonp
from src.common.web.flask_snippets import login_required
from src.common.web.flask_snippets import args_required
from src.config import BaseConfig

from flask import request
from flask import Blueprint
from flask import g
bucketName
reload(sys)
sys.setdefaultencoding('utf8')

video_bp = Blueprint('video', __name__)


@video_bp.route("/video/upload_init", methods=['GET'])
@jsonp
def upload_init():
    args = request.args
    key = http_util.check_params(args, 'video_name')
    if key:
        return http_util.return_param_not_found(key)

    client_ip = request.remote_addr

    res = video_client.upload_init(
        video_name=args['video_name'],
        client_ip=client_ip
    )

    if res:
        res['client_ip'] = client_ip
        return http_util.return_model(data=res)
    else:
        return http_util.return_internal_server_error()


@video_bp.route('/video/save', methods=['POST'])
@login_required
@args_required('url', 'poster')
def save_video():
    user_id = g.user_id
    args = request.json

    url = http_util.get_param(args, 'url', "")
    poster = http_util.get_param(args, 'poster', "")

    video = Video.create_video(
        user_id=user_id,
        url=url,
        poster=poster
    )

    # 记录用户上传视频
    Action.create_action(
        user_id=user_id,
        type=BaseConfig.TYPE_ACTION_UPLOAD,
        res_id=video.id,
        res_type=BaseConfig.TYPE_VIDEO_PLAY
    )

    detail = Video.get_video_detail(video.id)

    User.update_user_by_id(
        id=user_id,
        last_upload=detail
    )

    return http_util.return_model()


@video_bp.route('/video/related', methods=['GET'])
def related_video():
    args = request.args
    key = http_util.check_params(args, 'res_id')
    if key:
        return http_util.return_param_not_found(key)

    res_id = args.get('res_id')
    # TODO 需要真正的相关逻辑
    res = Video.query_related_videos(res_id)

    return http_util.return_model(
        data=res
    )
