#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''focus表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from sqlalchemy import desc

from src import db
from src.common.base import BaseBean
from src.config import BaseConfig


class HomePage(BaseBean, db.Model):
    __tablename__ = 'home_page'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    poster = db.Column(db.String, default="")
    url = db.Column(db.String, default="")
    res_id = db.Column(db.BIGINT)
    res_type = db.Column(db.Integer)
    type = db.Column(db.Integer)
    width_weight = db.Column(db.Float, default=1)
    position = db.Column(db.Integer, default=0)
    description = db.Column(db.String, default="")
    is_online = db.Column(db.Integer, default=1)
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_home_page(cls, **params):
        params['is_del'] = 0
        return HomePage.query.filter_by(**params).order_by(
            desc(HomePage.position)).first()

    @classmethod
    def query_home_pages(cls, **params):
        params['is_del'] = 0
        res = HomePage.query.filter_by(**params).order_by(
            desc(HomePage.position)).all()

        return res

    @classmethod
    def query_daily_resource(cls):
        return HomePage.query.filter_by(
            type=BaseConfig.TYPE_HOME_PAGE_DAILY_SHOW,
            is_del=0
        ).order_by(desc(HomePage.position)).first()

    @classmethod
    def query_home_page_paginate_by_type(cls, type, page, per_page):
        return HomePage.query.filter_by(
            type=type,
            is_del=0
        ).order_by(desc(HomePage.position)).paginate(page, per_page, False)

    @classmethod
    def query_home_page_paginate(cls, page, per_page, **params):
        if params:
            params['is_del'] = 0
        return HomePage.query.filter_by(**params).order_by(
            desc(HomePage.position)).paginate(page, per_page, False)

    @classmethod
    def update_home_page_by_id(cls, id, **params):
        hp = HomePage.query.filter_by(id=id, is_del=0).first()
        hp.name = params.get("name", hp.name)
        hp.poster = params.get("poster", hp.poster)
        hp.position = params.get("position", hp.position)
        hp.url = params.get("url", hp.url)
        hp.res_id = params.get("res_id", hp.res_id)
        hp.res_type = params.get("res_type", hp.res_type)
        hp.is_online = params.get("is_online", hp.is_online)
        hp.is_del = params.get("is_del", hp.is_del)
        hp.description = params.get("description", hp.description)
        db.session.commit()
        return hp

    @classmethod
    def create_home_page(cls, **params):
        hp = HomePage(**params)
        db.session.add(hp)
        db.session.commit()
        return hp


class ViewHotRes(BaseBean, db.Model):
    __tablename__ = 'view_hot_res'
    res_id = db.Column(db.String, primary_key=True)
    res_type = db.Column(db.INT)
    total = db.Column(db.INT)
    name = db.Column(db.String)
    poster = db.Column(db.String)
    description = db.Column(db.String)

    @classmethod
    def query_items(cls, **params):
        return cls.query.filter_by(**params).all()
