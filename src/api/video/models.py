#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import json

from elasticsearch.client import query_params
from sqlalchemy import desc

from src import db
from src import snowflake
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.pymysql_util import query
from src.common import utils


class Video(BaseBean, db.Model):
    __tablename__ = 'video'
    id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, default="")
    name = db.Column(db.String, default="")
    poster = db.Column(db.String, default="")
    letv_video_id = db.Column(db.String, default=0)
    letv_video_unique = db.Column(db.String, default="")
    url = db.Column(db.String(512), default="")
    type = db.Column(db.Integer, default=BaseConfig.TYPE_VIDEO_PLAY)
    status = db.Column(db.Integer, default=BaseConfig.TYPE_VIDEO_STATUS_NORMAL)
    description = db.Column(db.String, default="")
    is_del = db.Column(db.Integer, default=0)
    ext = db.Column(db.JSON, default={})
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_videos(cls, **params):
        if params:
            params['is_del'] = 0
        return Video.query.filter_by(**params).order_by(
            desc(Video.create_ts)).all()

    @classmethod
    def update_video_by_id(cls, id, **params):
        video = Video.query.get(id)
        video.status = params.get('status', video.status)
        video.name = params.get('name', video.name)
        video.poster = params.get('poster', video.poster)
        video.description = params.get('description', video.description)
        video.letv_video_id = params.get('letv_video_id', video.letv_video_id)
        video.letv_video_unique = params.get('letv_video_unique',
                                             video.letv_video_unique)
        video.url = params.get('url', video.url)
        video.type = params.get('type', video.type)
        video.is_del = params.get('is_del', video.is_del)
        db.session.commit()
        return video

    @classmethod
    def create_video(cls, **params):
        if params:
            params['id'] = snowflake.generate()
        v = Video(**params)
        db.session.add(v)
        db.session.commit()
        return v

    @classmethod
    def query_video_by_id(cls, id):
        return Video.query.filter_by(id=id, is_del=0).first()

    @classmethod
    def get_videos(cls):
        sql = "SELECT * FROM view_video"
        res = query(sql, [])
        map(utils.map_model_item, res)
        return res

    @classmethod
    def get_video_detail(cls, id):
        sql = "SELECT * FROM view_video WHERE res_id = %s;"

        res = query(sql, [id])
        if res:
            item = res[0]
            return utils.format_model_item(item)
        return None

    @classmethod
    def query_related_videos(cls, id):
        sql = "SELECT * FROM view_video where user_id <='' LIMIT 0,4;"

        res = query(sql,[])

        map(utils.map_model_item,res)

        return res

    @classmethod
    def query_user_last_video(cls, user_id):
        """查询用户最后上传视频"""
        return Video.query.filter_by(user_id=user_id).order_by(
            desc(Video.create_ts)).first()

    @classmethod
    def query_video_paginate(cls,page,per_page, **params):
        return Video.query.filter_by(**params).order_by(
            desc(Video.create_ts)).paginate(page, per_page, False)


def query_video_list(**params):
    return Video.query.filter_by(**params)


@query_params('status', 'is_del')
def update_video(video_id, params=None):
    """修改视频"""
    video = Video.query.get(video_id)
    video.status = params.get('status', video.status)
    db.session.commit()
