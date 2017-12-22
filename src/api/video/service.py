#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''视频逻辑模块'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys

from src.api.video.models import Video

reload(sys)
sys.setdefaultencoding('utf8')


def get_videos(**params):
    videos = Video.query_videos(**params)
    print(videos)

    items = []
    for item in videos:
        items.append(item.to_json())

    return items
