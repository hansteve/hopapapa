#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''audio表models'''

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


class Audio(BaseBean, db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    poster = db.Column(db.String, default="")
    url = db.Column(db.String(512), default="")
    description = db.Column(db.String, default="")
    is_online = db.Column(db.Integer, default=1)
    is_del = db.Column(db.Integer, default=0)
    ext = db.Column(db.JSON, default={})
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_audios(cls, **params):
        if params:
            params['is_del'] = 0
        return Audio.query.filter_by(**params).order_by(
            desc(Audio.create_ts)).all()

    @classmethod
    def update_audio_by_id(cls, id, **params):
        audio = Audio.query.filter_by(id=id, is_del=0).first()
        audio.name = params.get('name', audio.name)
        audio.poster = params.get('poster', audio.poster)
        audio.description = params.get('description', audio.description)
        audio.url = params.get('url', audio.url)
        audio.is_del = params.get('is_del', audio.is_del)
        audio.is_online = params.get('is_online', audio.is_online)
        db.session.commit()
        return audio

    @classmethod
    def create_audio(cls, **params):
        if params:
            params['id'] = snowflake.generate()
        v = Audio(**params)
        db.session.add(v)
        db.session.commit()
        return v

    @classmethod
    def get_audio_detail(cls, id):
        sql = 'select * from view_audio where res_id = %s'

        res = query(sql, [id])
        if res:
            item = res[0]
            return utils.format_model_item(item)

        return None

    @classmethod
    def get_items(cls):
        sql = 'select * from view_audio'
        res = query(sql, [])
        map(utils.map_model_item, res)
        return res

    @classmethod
    def query_audio_paginate(cls, page, per_page, **params):
        return Audio.query.filter_by(**params).order_by(
            desc(Audio.create_ts)).paginate(page, per_page, False)
