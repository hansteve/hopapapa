#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.video.models import Video
from src.common.http_util import return_model
from src.common.letv import video_client
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_video_bp = Blueprint('admin_video', __name__)


@admin_video_bp.route('/video/list.json', methods=['GET'])
@jsonp
def list():
    '''文章列表'''

    args = request.args

    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = Video.query_video_paginate(
        user_id="",
        is_del=0,
        page=page,
        per_page=per_page
    )

    videos = []
    for item in paginate.items:
        detail = item.to_json()
        # detail['id'] = "{}".format(detail['id'])
        videos.append(detail)

    res = http_util.make_page_response(videos, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_video_bp.route('/video/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def edit():
    '''创建文章'''
    args = request.form
    print(args)
    id = args.get('id', None)

    if id:
        Video.update_video_by_id(**args)
    else:
        print('create')
        Video.create_video(**args)

    return return_model()


@admin_video_bp.route("/video/upload_init.json", methods=['POST'])
@jsonp
def upload_init():
    args = request.args
    print(args)
    key = http_util.check_params(args, 'video_name')
    if key:
        return http_util.return_param_not_found(key)

    client_ip = request.remote_addr

    res = video_client.upload_init(
        video_name=args['video_name'],
        client_ip=client_ip,
        file_size=args['file_size'],
        uploadtype=args['uploadtype']
    )

    if res:
        res['client_ip'] = client_ip
        return http_util.return_model(data=res)
    else:
        return http_util.return_internal_server_error()
