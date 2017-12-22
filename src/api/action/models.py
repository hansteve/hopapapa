#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''action表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time

from sqlalchemy import desc

from src import db
from src.config import BaseConfig
from src.common.pymysql_util import query
from src.common.base import BaseBean


class Action(BaseBean, db.Model):
    __tablename__ = 'action'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    user_id = db.Column(db.String, default="")
    type = db.Column(db.Integer)
    res_id = db.Column(db.String)
    res_type = db.Column(db.Integer)
    ext = db.Column(db.JSON, default={})
    create_ts = db.Column(db.TIMESTAMP)

    # default = datetime.utcnow

    @classmethod
    def query_action(cls, **params):
        return Action.query.filter_by(**params).first()

    @classmethod
    def create_action(cls, **params):
        action = Action(**params)
        db.session.add(action)
        db.session.commit()
        return action

    @classmethod
    def query_actions(cls, **params):
        return Action.query.filter_by(**params).order_by(
            desc(Action.create_ts)).all()

    @classmethod
    def query_user_views(cls, user_id):
        actions = Action.query.filter_by(
            res_id=user_id,
            type=BaseConfig.TYPE_ACTION_VIEW
        ).all()
        return actions

    @classmethod
    def query_video_view_count(cls, video_id):
        return Action.query.filter_by(
            res_id=video_id,
            type=BaseConfig.TYPE_ACTION_VIEW
        )

    @classmethod
    def query_count(cls, **params):
        return Action.query.filter_by(**params).count()


def query_user_timeline(user_id, types, start, per_page):
    """查询用户时间线"""
    sql = "select * from action where type in %s and user_id = %s " \
          "and create_ts < %s order by create_ts desc limit 0,%s"

    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))

    return query(sql, [types, user_id, t, per_page])
