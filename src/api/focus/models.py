#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''focus表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from elasticsearch.client import query_params

from src import db
from src import snowflake
from src.config import BaseConfig
from src.common import utils
from src.common.base import BaseBean
from src.common.http_util import get_param
from src.common.http_util import get_param_int


class Focus(BaseBean, db.Model):
    __tablename__ = 'focus'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    name = db.Column(db.String)
    data = db.Column(db.JSON)
    type = db.Column(db.Integer)
    is_del = db.Column(db.Integer)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)


def query_focus_by_type(type):
    '''根据type查询focus'''
    return Focus.query.filter_by(type=type, is_del=0).first()
