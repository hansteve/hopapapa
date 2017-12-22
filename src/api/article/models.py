#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''文章表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src import snowflake
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.pymysql_util import query
from src.common import utils

from sqlalchemy import desc


class Article(BaseBean, db.Model):
    __tablename__ = 'article'
    id = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    poster = db.Column(db.String, default="")
    content = db.Column(db.String, default="")
    description = db.Column(db.String, default="")
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_article(cls, **params):
        if params:
            params['is_del'] = 0
        else:
            params = {
                "is_del": 0
            }
        return Article.query.filter_by(**params).first()

    @classmethod
    def query_articles(cls, **params):
        if params:
            params['is_del'] = 0
        return Article.query.filter_by(**params).order_by(
            desc(Article.create_ts)).all()

    @classmethod
    def query_article_paginate(cls, page, per_page, **params):
        if params:
            params['is_del'] = 0
        else:
            params = {'is_del': 0}
        return Article.query.filter_by(**params).order_by(
            desc(Article.create_ts)).paginate(page, per_page, False)

    @classmethod
    def create_article(cls, **params):
        if params:
            params['id'] = snowflake.generate()

        a = Article(**params)
        db.session.add(a)
        db.session.commit()
        return a

    @classmethod
    def get_article_detail(cls, id):
        sql = 'SELECT * FROM view_article WHERE res_id = %s;'

        res = query(sql, [id])
        if res:
            item = res[0]
            return utils.format_model_item(item)
        else:
            return None

    @classmethod
    def get_articles(cls):
        sql = 'SELECT * FROM view_article'

        res = query(sql, [])

        map(utils.map_model_item, res)
        return res

    @classmethod
    def update_article_by_id(cls, id, **params):
        a = Article.query.get(id)
        a.name = params.get('name', a.name)
        a.poster = params.get('poster', a.poster)
        a.description = params.get('description', a.description)
        a.is_del = params.get('is_del', a.is_del)

        db.session.commit()
        return a

    def query_article_by_id(article_id):
        '''根据id查询文章'''
        return Article.query.get(article_id)
