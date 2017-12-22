#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''collection表models'''

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


class Collection(BaseBean, db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    poster = db.Column(db.String, default="")
    description = db.Column(db.String, default="")
    ext = db.Column(db.JSON, default={})
    is_offline = db.Column(db.Integer, default=0)
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_paginate(cls, page, per_page, **params):
        if params:
            params['is_del'] = 0
        else:
            params = {
                "is_del": 0
            }
        return cls.query.filter_by(**params).order_by(
            desc(cls.create_ts)).paginate(page, per_page, False)

    @classmethod
    def update_by_id(cls, id, **params):
        item = cls.query.filter_by(id=id, is_del=0).first()
        item.name = params.get('name', item.name)
        item.poster = params.get('poster', item.poster)
        item.description = params.get('description', item.description)
        item.is_del = params.get('is_del', item.is_del)
        item.is_offline = params.get('is_offline', item.is_offline)
        db.session.commit()
        return item

    @classmethod
    def create(cls, **params):
        if params:
            params['id'] = snowflake.generate()
        v = cls(**params)
        db.session.add(v)
        db.session.commit()
        return v

    @classmethod
    def get_collection_detail(cls, id):
        sql = "select * from view_collection where res_id = %s;"
        res = query(sql, [id])
        if res:
            item = res[0]
            item = utils.format_model_item(item)
            return item
        else:
            return None

    @classmethod
    def get_items(cls,):
        sql = "select * from view_collection"
        res = query(sql, [])
        map(utils.map_model_item, res)
        return res


class CollectionResource(BaseBean, db.Model):
    __tablename__ = 'collection_resource'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    collection_id = db.Column(db.String)
    res_id = db.Column(db.String)
    res_type = db.Column(db.Integer)
    position = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def create(cls, **params):
        v = cls(**params)
        db.session.add(v)
        db.session.commit()
        return v

    @classmethod
    def update_by_id(cls, id, **params):
        item = cls.query.filter_by(id=id).first()
        item.res_id = params.get('res_id', item.res_id)
        item.res_type = params.get('res_type', item.res_type)
        item.position = params.get('position', item.position)
        db.session.commit()
        return item

    @classmethod
    def query_items(cls, **params):
        return cls.query.filter_by(**params).order_by(
            desc(CollectionResource.position)).all()

    @classmethod
    def query_paginate(cls, page, per_page, **params):
        return cls.query.filter_by(**params).order_by(
            desc(cls.create_ts)).paginate(page, per_page, False)

    @classmethod
    def delete(cls, **params):
        dr = cls.query.filter_by(**params).first()
        db.session.delete(dr)
        db.session.commit()
