#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''article表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import app
from src import env_config
from src.common import utils
from src.api.article import models
from src.api.article.models import Article
from src.common.http_util import return_model
from src.common.web.flask_snippets import jsonp

from flask import Blueprint

article_bp = Blueprint('article', __name__)


@article_bp.route('/article/<string:article_id>', methods=['GET'])
@jsonp
def get_article(article_id):
    '''获取文章内容'''
    a = Article.query_article(id=article_id)

    item = a.to_json()

    item['article_id'] = item['id']
    item['create_ts'] = utils.make_timestamp_for_sql_time(item['create_ts'])

    del item['id']
    del item['is_del']
    del item['update_ts']
    return return_model(
        data=item
    )

