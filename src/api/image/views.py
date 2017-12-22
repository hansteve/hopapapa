#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''图片逻辑模块'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys

from src.common import http_util
from src.config import BaseConfig
from src.common.web.flask_snippets import login_required
from src.common.web.flask_snippets import args_required
from src.api.image import models as image_db
from src.api.image.models import Image
from src.api.user.models import User
from src.api.action.models import Action

from flask import request
from flask import Blueprint
from flask import g

reload(sys)
sys.setdefaultencoding('utf8')

image_bp = Blueprint('image', __name__)


@image_bp.route('/image/save', methods=['POST'])
@login_required
@args_required('urls')
def save_image():
    user_id = g.user_id
    args = request.json
    urls = http_util.get_param(args, 'urls')

    if urls:
        for url in urls:
            image = image_db.create_image(user_id=user_id, url=url)
            # 记录用户上传图片行为
            Action.create_action(
                user_id=user_id,
                type=BaseConfig.TYPE_ACTION_UPLOAD,
                res_id=image.id,
                res_type=BaseConfig.TYPE_IMAGE
            )

            detail = Image.get_image_detail(image.id)
            User.update_user_by_id(
                id=user_id,
                last_upload=detail
            )
        return http_util.return_model()
    else:
        return http_util.return_param_not_found('urls')
