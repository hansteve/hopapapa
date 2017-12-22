#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''restless逻辑'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from flask_restless import APIManager

from src import app
from src import db
from src.api.user.models import User
from src.api.video.models import Video
from src.api.article.models import Article
from src.api.home_page.models import HomePage
from src.api.audio.models import Audio
from src.api.collection.models import Collection
from src.api.collection.models import CollectionResource
from src.api.sensitive_word.models import SensitiveWord
from src.admin.user.views import admin_user_bp
from src.admin.video.views import admin_video_bp
from src.admin.image.views import admin_image_bp
from src.admin.home_page.views import admin_home_page_bp
from src.admin.article.views import admin_article_bp
from src.admin.audio.views import admin_audio_bp
from src.admin.push.views import admin_push_bp
from src.admin.collection.views import admin_collection_bp
from src.admin.search.views import admin_search_bp
from src.admin.sensitive_word.views import admin_sensitive_word_bp
from src.config import BaseConfig

URL_PREFIX = BaseConfig.APPLICATION_ROOT_ADMIN

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, url_prefix=URL_PREFIX, methods=['GET'])
manager.create_api(Video, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH'])
manager.create_api(Article, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH'])
manager.create_api(HomePage, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH'])
manager.create_api(Audio, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
manager.create_api(Collection, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
manager.create_api(CollectionResource, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
manager.create_api(SensitiveWord, url_prefix=URL_PREFIX,
                   methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])

# admin bluprint
app.register_blueprint(admin_article_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_image_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_video_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_home_page_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_audio_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_push_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_collection_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_user_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_search_bp, url_prefix=URL_PREFIX)
app.register_blueprint(admin_sensitive_word_bp, url_prefix=URL_PREFIX)
