#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.audio.models import Audio
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_audio_bp = Blueprint('admin_audio', __name__)


@admin_audio_bp.route('/audio/list.json', methods=['GET'])
@jsonp
def list():
    '''文章列表'''

    args = request.args
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = Audio.query_audio_paginate(
        page=page,
        per_page=per_page,
        is_del=0
    )

    videos = []
    for item in paginate.items:
        detail = item.to_json()
        videos.append(detail)

    res = http_util.make_page_response(videos, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_audio_bp.route('/audio/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def edit():
    '''创建文章'''
    args = request.form
    id = args.get('id', None)

    if id:
        audio = Audio.update_audio_by_id(**args)
    else:
        Audio.create_audio(**args)

    return return_model()
