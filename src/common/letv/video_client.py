#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''letv 点播工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.config import BaseConfig
from src.common.letv import utils as letv_utils

from elasticsearch.client import query_params


@query_params('client_ip','uploadtype','file_size')
def upload_init(video_name, params=None):
    api = 'video.upload.init'

    if params:
        params['video_name'] = video_name
    else:
        params = {'video_name': video_name}

    params['isdownload'] = 1

    return letv_utils.post(
        url=BaseConfig.LETV_VIDEO_API_URL,
        api=api,
        params=params
    )


def get_video(video_id):
    api = 'video.get'

    return letv_utils.post(
        url=BaseConfig.LETV_VIDEO_API_URL,
        api=api,
        params={"video_id": video_id}
    )


