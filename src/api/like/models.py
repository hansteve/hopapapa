#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''like表models'''
from sqlalchemy import text

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src.config import BaseConfig
from src.common.base import BaseBean


class LikeInfo(BaseBean, db.Model):
    __tablename__ = 'like_info'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    user_id = db.Column(db.String)
    res_id = db.Column(db.String)
    res_type = db.Column(db.Integer)
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_like(cls, **params):
        if params:
            params['is_del'] = 0
        return LikeInfo.query.filter_by(**params).first()

    @classmethod
    def query_count(cls, **params):
        if params:
            params['is_del'] = 0
        return LikeInfo.query.filter_by(**params).count()

    @classmethod
    def create_like(cls, **params):
        info = LikeInfo(**params)
        db.session.add(info)
        db.session.commit()
        return info

    @classmethod
    def update_like(cls, **params):
        info = LikeInfo.query.filter_by(**params).first()
        info.is_del = params.get('is_del', info.is_del)
        db.session.commit()
        return info

    @classmethod
    def dis_like(cls, user_id, res_id, res_type):
        '''取消点赞'''
        sql = 'update like_info set is_del = 1 WHERE ' \
              'user_id = :user_id AND res_id = :res_id ' \
              'AND res_type = :res_type'

        db.engine.execute(
            text(sql),
            user_id=user_id,
            res_id=res_id,
            res_type=res_type,
        )
