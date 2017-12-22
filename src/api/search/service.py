#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''search service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.api.user.models import User
from src.api.video.models import Video
from src.api.article.models import Article
from src.api.collection.models import Collection
from src.api.audio.models import Audio
from src.common import aws_es as es
from src.config import BaseConfig


class Search():
    @classmethod
    def sync_index_by_id(cls, res_id, res_type):
        """根据id刷新索引"""
        item = None
        if res_type == BaseConfig.TYPE_USER:
            item = User.get_detail(res_id)

        args = make_search_args(res_type)
        args['id'] = item['res_id']
        item = format_item(item)
        args['body'] = item
        print(args)
        es.sync_index(**args)


def sync_index_all():
    types = [
        BaseConfig.TYPE_USER, BaseConfig.TYPE_COLLECTION,
        BaseConfig.TYPE_VIDEO_PLAY, BaseConfig.TYPE_AUDIO,
        BaseConfig.TYPE_ARTICLE
    ]

    for type in types:
        sync_index_by_type(type)


def sync_index_by_type(type):
    """根据type刷新索引"""
    args = make_search_args(type)
    items = []
    if type == BaseConfig.TYPE_USER:
        items = User.get_normal_users()
    elif type == BaseConfig.TYPE_VIDEO_PLAY:
        items = Video.get_videos()
    elif type == BaseConfig.TYPE_ARTICLE:
        items = Article.get_articles()
    elif type == BaseConfig.TYPE_AUDIO:
        items = Audio.get_items()
    elif type == BaseConfig.TYPE_COLLECTION:
        items = Collection.get_items()
    else:
        return False

    es.delete_index_by_type(**args)
    for item in items:
        args['id'] = item['res_id']
        item = format_item(item)
        args['body'] = item
        es.sync_index(**args)


def format_item(item):
    type = item['res_type']
    item[BaseConfig.ES_PARAMS_WEIGHT] = BaseConfig.ES_ENUM.get(type).get(
        'weight')
    return item


def make_index_id(item, type):
    """生成索引id"""
    field = BaseConfig.ES_ENUM.get(type).get("id")
    return item[field]


def make_search_args(type):
    """生成索引参数"""
    doc_type = BaseConfig.ES_ENUM.get(type).get("doc_type")
    return {
        "index": BaseConfig.ES_INDEX,
        "doc_type": doc_type
    }
