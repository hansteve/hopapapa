#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''首页逻辑模块'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys
import os

from src.config import BaseConfig
from src.common import http_util
from src.api.focus import models as focus_db
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint
from flask import make_response
from flask import send_file

reload(sys)
sys.setdefaultencoding('utf8')

support_bp = Blueprint('support', __name__)


@support_bp.route('/test', methods=['GET', 'POST'])
@jsonp
def test():
    '''一级页面接口'''
    print(request.method)

    print(request.content_type)

    # application / x - www - form - urlencoded
    # application / x - www - form - urlencoded

    return http_util.return_model(
        data={
            'form': request.form,
            'json': request.json
        }
    )


@support_bp.route('/apple-app-site-association', methods=['GET'])
@jsonp
def apple():
    '''一级页面接口'''
    response = make_response(send_file(
        "static/apple-app-site-association"))
    return response
