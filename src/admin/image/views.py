#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''图片逻辑代码'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time

from src.config import BaseConfig
from src.common.aliyun_util import put_object
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain

from flask import request
from flask import Blueprint
from flask import render_template

admin_image_bp = Blueprint('admin_image', __name__)


@admin_image_bp.route('/upload/image', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def upload_image():
    files = request.files
    print(files)

    for file in files:
        print(file)

    file = request.files['file']
    filename = file.filename
    suffix = filename.rsplit('.', 1)[1]
    print(filename)

    datetime_root = time.strftime("%Y%m%d/%H/%M%S", time.localtime())

    url = put_object(
        key='{}/{}.{}'.format(datetime_root, int(time.time()), suffix),
        data=file,
        bucket_name=BaseConfig.ALIYUN_BUCKET_IMG
    )
    return return_model(
        data={"url": url}
    )


@admin_image_bp.route('/image/upload', methods=['GET'])
def upload_html():
    print('upload')
    return render_template('image/upload.html')
