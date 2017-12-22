#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.search.service import sync_index_by_type
from src.api.search.service import sync_index_all
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp
from src.common.web.flask_snippets import args_required

from flask import request
from flask import Blueprint

admin_search_bp = Blueprint('admin_search', __name__)


@admin_search_bp.route('/search/sync_index.json', methods=['GET'])
@jsonp
@args_required('type')
def sync_index():
    '''刷新索引'''
    args = request.args

    type = http_util.get_param_int(args, 'type', -1)

    if type == -1:
        sync_index_all()
    else:
        sync_index_by_type(type)
    return return_model()
