#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''restless逻辑'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from flask import g
from flask import request

from src import app
from src.api.user.models import User
from src.api.user.views import user_bp
from src.api.code.views import code_bp
from src.api.like.views import like_bp
from src.api.article.views import article_bp
from src.api.comment.views import comment_bp
from src.api.video.views import video_bp
from src.api.image.views import image_bp
from src.api.home_page.views import home_page_bp
from src.api.location.views import location_bp
from src.api.support.views import support_bp
from src.api.push.views import push_bp
from src.api.search.views import search_bp
from src.config import BaseConfig
from src.common.http_util import get_login_user_id


@app.before_request
def init_request():
    g.user = None
    g.user_id = None
    user_id = get_login_user_id(request)
    if user_id:
        g.user = User.query_user(id=user_id)
        if g.user:
            g.user_id = g.user.id


URL_PREFIX = BaseConfig.APPLICATION_ROOT
# api blueprint
app.register_blueprint(article_bp, url_prefix=URL_PREFIX)
app.register_blueprint(code_bp, url_prefix=URL_PREFIX)
app.register_blueprint(comment_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_page_bp, url_prefix=URL_PREFIX)
app.register_blueprint(image_bp, url_prefix=URL_PREFIX)
app.register_blueprint(like_bp, url_prefix=URL_PREFIX)
app.register_blueprint(location_bp, url_prefix=URL_PREFIX)
app.register_blueprint(user_bp, url_prefix=URL_PREFIX)
app.register_blueprint(video_bp, url_prefix=URL_PREFIX)
app.register_blueprint(push_bp, url_prefix=URL_PREFIX)
app.register_blueprint(search_bp, url_prefix=URL_PREFIX)
app.register_blueprint(support_bp)
