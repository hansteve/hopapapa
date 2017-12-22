#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''location表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.pymysql_util import query

from sqlalchemy import desc


class Location(BaseBean, db.Model):
    __tablename__ = 'location'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    user_id = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    create_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def get_user_last_location_time(cls, user_id):
        '''查询用户最后的位置'''
        sql = 'select * from view_last_location_time where user_id = %s'
        res = query(sql, [user_id])
        if res:
            return res[0]['create_ts']
        else:
            return 0


def create_location(user_id, lat, lng):
    '''创建地理位置'''
    location = Location(
        user_id=user_id,
        lat=lat,
        lng=lng
    )
    db.session.add(location)
    db.session.commit()
    return location


def query_user_last_location(user_id):
    '''查询用户最后的位置'''
    return Location.query.filter_by(user_id=user_id).order_by(
        desc(Location.create_ts)).first()
