#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''code表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src.config import BaseConfig
from src.common.http_util import return_model
from src.common.http_util import check_params
from src.common.wangyi import sms

from sqlalchemy import text
from flask import request
from flask import Blueprint

code_bp = Blueprint('code', __name__)


@code_bp.route('/code/send', methods=['POST'])
def send_code():
    '''发送验证码'''
    json = request.json
    print(json)
    key = check_params(json, 'mobile')
    if key:
        return return_model(message='{} not found'.format(key), status=400)

    mobile = json['mobile']
    del_sql = 'UPDATE code SET is_del = 1 WHERE mobile = :mobile;'
    db.engine.execute(text(del_sql), mobile=mobile)

    # code = create_code_by_mobile(mobile)

    code = sms.send_code(
        mobile=mobile,
        templateid=BaseConfig.CODE_TEMPLATE_ID1
    )

    if code:
        return return_model()
    else:
        return return_model(status=500, message='发送失败')
