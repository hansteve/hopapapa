#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''location表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.api.push.models import Push
from src.common import http_util

from flask import Blueprint

push_bp = Blueprint('push', __name__)


@push_bp.route('/push/list', methods=['GET'])
def push_list():
    '''系统消息列表'''

    res = Push.get_pushs()

    return http_util.return_model(res)
