#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''push表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.pymysql_util import query

from sqlalchemy import desc


class Push(BaseBean, db.Model):
    __tablename__ = 'push'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    description = db.Column(db.String)
    open_type = db.Column(db.Integer)
    res_id = db.Column(db.String, default="")
    res_type = db.Column(db.Integer, default=0)
    url = db.Column(db.String, default="")
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def create_push(cls, **params):
        p = Push(**params)
        db.session.add(p)
        db.session.commit()

        return p

    @classmethod
    def query_pushs(cls, **params):
        if params:
            params['is_del'] = 0
        else:
            params = {
                'is_del': 0
            }
        return Push.query.filter_by(**params).order_by(
            desc(Push.create_ts)).all()

    @classmethod
    def query_paginate(cls, page, per_page, **params):
        if params:
            params['is_del'] = 0
        else:
            params = {
                'is_del': 0
            }
        return Push.query.filter_by(**params).order_by(
            desc(Push.create_ts)).paginate(page, per_page, False)

    @classmethod
    def get_pushs(cls):
        sql = "select * from view_push"

        return query(sql, [])

    @classmethod
    def update_push_by_id(cls, id, **params):
        push = Push.query.filter_by(id=id, is_del=0).first()
        push.name = params.get('name', push.name)
        push.description = params.get('description', push.description)
        push.url = params.get('url', push.url)
        push.is_del = params.get('is_del', push.is_del)
        db.session.commit()
        return push
