#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''base工具'''
from sqlalchemy import desc

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import json
from datetime import datetime, date
from uuid import UUID
from sqlalchemy.ext.declarative import DeclarativeMeta

from src import db


class BaseBean(object):
    """
    SQLAlchemy JSON serialization
    """
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json_str(self, rel=None):
        '''输出json字符串'''

        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
            if isinstance(x, date):
                return x.isoformat()

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)

    def to_json(self, rel=None):
        '''输出json'''
        return json.loads(self.to_json_str(rel=rel))

    @classmethod
    def create(cls, **params):
        item = cls(**params)
        db.session.add(item)
        db.session.commit()
        return item

    @classmethod
    def query_item(cls, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        return cls.query.filter_by(**params).first()

    @classmethod
    def query_items(cls, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        return cls.query.filter_by(**params).order_by(desc(cls.create_ts)).all()

    @classmethod
    def query_paginate(cls, page, per_page, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        return cls.query.filter_by(**params).order_by(
            desc(cls.create_ts)).paginate(page, per_page, False)

    @classmethod
    def query_count(cls, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        return cls.query.filter_by(**params).count()

    @classmethod
    def delete(cls, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        item = cls.query.filter_by(**params).first()
        item.is_del = 1
        return item
