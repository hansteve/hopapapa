#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''image表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from elasticsearch.client import query_params

from src import db
from src import snowflake
from src.config import BaseConfig
from src.common import utils
from src.common.base import BaseBean
from src.common.http_util import get_param
from src.common.pymysql_util import query


class Image(BaseBean, db.Model):
    __tablename__ = 'image'
    id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, default="")
    name = db.Column(db.String, default="")
    url = db.Column(db.String)
    ext = db.Column(db.JSON)
    description = db.Column(db.String, default="")
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def update_image_by_id(cls, id, **params):
        image = Image.query.filter_by(id=id, is_del=0).first()
        image.is_del = params.get('is_del', Image.is_del)
        image.url = params.get('url', Image.url)
        image.name = params.get('name', Image.name)
        image.description = params.get('description', Image.description)

        db.session.commit()
        return image

    @classmethod
    def get_image_detail(cls, id):
        sql = "select * from view_image where res_id = %s;"
        res = query(sql, [id])
        if res:
            item = res[0]
            item = utils.format_model_item(item)
            return item
        else:
            return None


@query_params('user_id', 'url')
def create_image(params=None):
    user_id = get_param(params, 'user_id', 0)
    url = get_param(params, 'url', '')

    v = Image(
        id=snowflake.generate(),
        user_id=user_id,
        url=url,
        is_del=BaseConfig.DEFAULT_IS_DEL,
    )

    db.session.add(v)
    db.session.commit()
    return v


def query_image_by_id(id):
    return Image.query.filter_by(id=id, is_del=0).first()

