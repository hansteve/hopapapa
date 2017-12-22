#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''初始化程序'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import os
import time
import logging

from flask import g
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string
from werkzeug.contrib.fixers import ProxyFix

from src.common.id_util import Snowflake

CONFIG_NAME_MAPPER = {
    'local': 'src.local_config.LocalConfig',
    'prod': 'src.local_config.ProductionConfig',
    'dev': 'src.local_config.DevelopmentConfig',
    'test': 'src.local_config.TestingConfig'
}


def create_app(flask_config_name=None):
    """
    创建配置
    :return:
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    env_flask_config_name = os.getenv('FLASK_CONFIG')

    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = 'local'
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name

    config_name = CONFIG_NAME_MAPPER[flask_config_name]

    app.config.from_object(config_name)
    # app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4_unicode_ci'

    print('-------------------------init app-------------------------')
    env_config = import_string(config_name)

    logging.basicConfig(
        filename=env_config.METRICS_LOG_FILE, level=logging.ERROR)
    return app, env_config


app, env_config = create_app()


# metrics only begin by wenxiaoning
@app.before_request
def before_request():
    g.request_start_time = time.time()

    req_method = request.method

    if req_method == 'POST':
        app.logger.debug(
            '{} {} json:{}\nform:{}'.format(req_method, request.url,
                                            request.json, request.form))
    elif req_method == 'GET':
        app.logger.debug(
            '{} {} args:{}'.format(req_method, request.url, request.args))



@app.after_request
def after_request(response):
    if not hasattr(g, 'request_start_time'):
        return response

    elapsed = time.time() - g.request_start_time
    elapsed = int(round(1000 * elapsed))

    req_info = str(
        g.request_start_time) + "_" + request.method + "_" + request.url
    logging.debug(req_info + ":" + str(elapsed))

    return response


# app.before_request(before_request)
# app.after_request(after_request)
# metrics only end


db = SQLAlchemy(app)

snowflake = Snowflake(0)
