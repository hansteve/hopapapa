#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''sensitive 表models'''
from sqlalchemy import text

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from datetime import datetime

from src import db
from src.config import BaseConfig
from src.common.base import BaseBean


class SensitiveWord(BaseBean, db.Model):
    __tablename__ = 'sensitive_word'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    content = db.Column(db.String)
    is_del = db.Column(db.INT,default=0)
    create_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    update_ts = db.Column(db.TIMESTAMP, default=datetime.utcnow)

    @classmethod
    def update_by_id(cls, id, **params):
        item = cls.query.filter_by(id=id, is_del=0).first()
        item.content = params.get('content', item.content)
        item.is_del = params.get('is_del', item.is_del)
        db.session.commit()
        return item
