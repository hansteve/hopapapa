#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''首页逻辑模块'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys

from src import app
from src.config import BaseConfig
from src.api.article.models import Article
from src.api.audio.models import Audio
from src.api.action.models import Action
from src.api.comment.models import Comment
from src.api.comment.service import get_comments
from src.api.collection.models import Collection
from src.api.collection.models import CollectionResource
from src.api.home_page.models import HomePage
from src.api.home_page.models import ViewHotRes
from src.api.image.models import Image
from src.api.video.models import Video
from src.api.like.models import LikeInfo
from src.api.push.models import Push
from src.common.base import BaseBean

from flask import g
from flask.ext.sqlalchemy import Pagination

reload(sys)
sys.setdefaultencoding('utf8')


class Resource(BaseBean):
    @classmethod
    def get_resource_detail(cls, res_id, res_type, source_include=[], **params):
        """获取资源详情"""
        detail = None
        login_user_id = g.user_id
        if res_type == BaseConfig.TYPE_VIDEO_PLAY:
            detail = Video.get_video_detail(res_id)
        elif res_type == BaseConfig.TYPE_ARTICLE:
            detail = Article.get_article_detail(res_id)
            if not detail:
                app.logger.error('{} not found'.format(res_id))
                return None
            del detail['content']
        elif res_type == BaseConfig.TYPE_AUDIO:
            detail = Audio.get_audio_detail(res_id)
        elif res_type == BaseConfig.TYPE_IMAGE:
            detail = Image.get_image_detail(res_id)
        elif res_type == BaseConfig.TYPE_COLLECTION:
            detail = Collection.get_collection_detail(res_id)
            subs = []
            if 'items' in source_include:
                items = CollectionResource.query_items(collection_id=res_id)
                for item in items:
                    sub_id = item.res_id
                    sub_type = item.res_type

                    sub_detail = Resource.get_resource_detail(
                        res_id=sub_id,
                        res_type=sub_type,
                        source_include=['comment_count', 'view_count',
                                        'like_count'],
                        login_user_id=login_user_id
                    )
                    if sub_detail:
                        subs.append(sub_detail)
            detail['items'] = subs

        if not detail:
            return None

        # 添加评论
        if 'comments' in source_include:
            comments = get_comments(
                res_id=res_id,
                start=BaseConfig.MAX_START,
                per_page=5
            )
            detail['comments'] = comments

        # 相关视频
        if 'related_items' in source_include and res_type != BaseConfig.TYPE_COLLECTION:
            related_videos = Video.query_related_videos(res_id)
            detail['related_items'] = related_videos

        ext = detail.get('ext', {})
        # 观看数量
        if 'view_count' in source_include:
            count = Action.query_count(
                type=BaseConfig.TYPE_ACTION_VIEW,
                res_id=res_id
            )
            ext['view_count'] = count

        # 点赞数量
        if 'like_count' in source_include:
            count = LikeInfo.query_count(
                res_id=res_id,
                res_type=res_type
            )
            ext['like_count'] = count

        # 评论数量
        if 'comment_count' in source_include:
            count = Comment.query_count(
                res_id=res_id,
                res_type=res_type
            )
            ext['comment_count'] = count

        detail['ext'] = ext

        # 关注状态
        detail['is_like'] = 0
        if login_user_id:
            is_like = LikeInfo.query_like(
                user_id=login_user_id,
                res_id=res_id,
                res_type=res_type
            )
            if is_like:
                detail['is_like'] = 1
        return detail

    @classmethod
    def get_resource_list(cls, res_type):
        res = []
        if res_type == BaseConfig.TYPE_VIDEO_PLAY:
            res = Video.get_videos()
        elif res_type == BaseConfig.TYPE_ARTICLE:
            res = Article.get_articles()

        return res

    @classmethod
    def delete_resource(cls, res_id, res_type):
        res = None
        if res_type == BaseConfig.TYPE_VIDEO_PLAY:
            res = Video.update_video_by_id(
                id=res_id,
                is_del=1
            )
        elif res_type == BaseConfig.TYPE_ARTICLE:
            res = Article.update_article_by_id(
                id=res_id,
                is_del=1
            )
        elif res_type == BaseConfig.TYPE_IMAGE:
            res = Image.update_image_by_id(
                id=res_id,
                is_del=1
            )
        elif res_type == BaseConfig.TYPE_AUDIO:
            res = Audio.update_audio_by_id(
                id=res_id,
                is_del=1
            )
        elif res_type == BaseConfig.TYPE_PUSH:
            res = Push.update_push_by_id(
                id=res_id,
                is_del=1
            )
        elif res_type == BaseConfig.TYPE_COLLECTION:
            res = Collection.update_by_id(
                id=res_id,
                is_del=1
            )

        return res

    @classmethod
    def change_online_status(cls, res_id, res_type, is_online):
        res = None
        if res_type == BaseConfig.TYPE_VIDEO_PLAY:
            res = Video.update_video_by_id(
                id=res_id,
                is_online=is_online
            )
        elif res_type == BaseConfig.TYPE_ARTICLE:
            res = Article.update_article_by_id(
                id=res_id,
                is_online=is_online
            )
        elif res_type == BaseConfig.TYPE_IMAGE:
            res = Image.update_image_by_id(
                id=res_id,
                is_online=is_online
            )
        elif res_type == BaseConfig.TYPE_AUDIO:
            res = Audio.update_audio_by_id(
                id=res_id,
                is_online=is_online
            )

        return res

    @classmethod
    def check_resource_use_status(cls, res_id, res_type):
        hp = HomePage.query_home_page(
            res_id=res_id,
            res_type=res_type
        )
        if hp:
            return '该资源正在使用中'
        return None

    @classmethod
    def get_show_resource(cls, login_user_id):
        hp = HomePage.query_daily_resource()

        if hp:
            hp_show = Resource.get_resource_detail(hp.res_id, hp.res_type)
            if hp_show:
                # 记录用户查看状态
                if login_user_id:
                    is_exists = Action.query_action(
                        user_id=login_user_id,
                        type=BaseConfig.TYPE_ACTION_VIEW_HOME_PAGE_SHOW,
                        res_id=hp_show['res_id'],
                        res_type=hp_show['res_type']
                    )
                    if is_exists:
                        return None

                    Action.create_action(
                        user_id=login_user_id,
                        type=BaseConfig.TYPE_ACTION_VIEW_HOME_PAGE_SHOW,
                        res_id=hp_show['res_id'],
                        res_type=hp_show['res_type']
                    )

                return hp_show

        return None

    @classmethod
    def get_home_page_paginate(cls, type, page, per_page):
        paginate = HomePage.query_home_page_paginate(
            type=type,
            page=page,
            is_online=1,
            per_page=per_page
        )
        items = Resource.format_paginate_items(paginate)
        return Pagination(None, page, per_page, paginate.total, items)

    @classmethod
    def format_paginate_items(cls, paginate):

        datas = paginate.items
        return cls.format_items(datas)

    @classmethod
    def format_items(cls, items):
        res = []
        for data in items:
            detail = Resource.get_resource_detail(
                res_id=data.res_id,
                res_type=data.res_type,
                source_include=['comment_count', 'view_count', 'like_count']
            )
            if detail:
                detail = cls.format_detail(data, detail)
                res.append(detail)
        return res

    @classmethod
    def format_detail(cls, data, detail):
        if data.name:
            detail['name'] = data.name

        if data.poster:
            detail['poster'] = data.poster

        if data.description:
            detail['description'] = data.description

        return detail

    @classmethod
    def get_hot_items(cls):
        items = ViewHotRes.query_items()
        return Resource.format_items(items[0:5])


    @classmethod
    def get_carousels(cls):
        pass

    @classmethod
    def get_home_page(cls):
        pass
