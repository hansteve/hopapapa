#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''letv常量'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."


"""
视频状态：
10表示可以正常播放；
20表示转码失败；
21表示审核失败；
22表示片源错误；
23表示发布失败；
24表示上传失败；
30表示正在处理过程中；
31表示正在审核过程中；
32表示无视频源；
33表示正在上传初始化；
34表示正在上传过程中；
40表示停
"""

VIDEO_STATUS_NORMAL = 10
VIDEO_STATUS_TRANSCODING_ERROR = 20
