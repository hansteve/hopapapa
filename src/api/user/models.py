#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户表models'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from elasticsearch.client import query_params
from sqlalchemy import text
from sqlalchemy import desc

from src import db
from src import snowflake
from src.config import BaseConfig
from src.common import utils
from src.common.base import BaseBean
from src.common.http_util import get_param
from src.common.pymysql_util import query


class User(BaseBean, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String, primary_key=True, unique=True)
    name = db.Column(db.String, default="")
    mobile = db.Column(db.String, default="")
    portrait = db.Column(db.String, default=BaseConfig.DEFAULT_PORTRAIT)
    gender = db.Column(db.Float, default=BaseConfig.DEFAULT_GENDER)
    age = db.Column(db.Integer, default=BaseConfig.DEFAULT_AGE)
    status = db.Column(db.Integer, default=BaseConfig.TYPE_USER_NORMAL)
    is_del = db.Column(db.Integer, default=0)
    banner = db.Column(db.JSON, default={})
    last_upload = db.Column(db.JSON, default={})
    ext = db.Column(db.JSON, default={
        "location": "",
        "sign": "",
        "lat": 0,
        "lng": 0
    })
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    # 外链
    opens = db.relationship('UserOpen', backref='user',
                            lazy='dynamic')

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
    def query_user(cls, **params):
        if params:
            params['is_del'] = 0
        return cls.query.filter_by(**params).first()

    @classmethod
    def query_items(cls, **params):
        if not params:
            params = {}
        params['is_del'] = 0
        return cls.query.filter_by(**params).order_by(desc(cls.create_ts)).all()

    @classmethod
    def get_detail(cls, id):
        sql = 'select * from view_user where user_id = %s;'
        res = query(sql, [id])
        if res:
            item = res[0]
            return utils.format_model_item(item)
        return None

    @classmethod
    def get_normal_users(cls):
        sql = "SELECT * FROM view_user WHERE status = 52;"
        res = query(sql, [])
        map(utils.map_model_item, res)
        return res

    @classmethod
    def create_user(cls, **params):
        if params:
            params['id'] = snowflake.generate()
        user = User(**params)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def create_anonymous_user(cls):
        '''创建匿名用户'''
        name = '匿名{}'.format(utils.get_random_num(5))
        return User.create_user(
            name=name,
            status=BaseConfig.TYPE_USER_ANONYMOUS
        )

    @classmethod
    def update_user_by_id(cls, id, **params):
        '''根据用户id修改信息'''
        u = User.query.get(id)
        u.name = get_param(params, 'name', u.name)
        u.mobile = get_param(params, 'mobile', u.mobile)
        u.portrait = get_param(params, 'portrait', u.portrait)
        u.gender = get_param(params, 'gender', u.gender)
        u.age = get_param(params, 'age', u.age)
        u.status = get_param(params, 'status', u.status)
        u.is_del = get_param(params, 'is_del', u.is_del)

        ext = u.ext
        location = get_param(params, 'location', ext['location'])
        sign = get_param(params, 'sign', ext['sign'])
        lat = get_param(params, 'lat', ext['lat'])
        lng = get_param(params, 'lng', ext['lng'])

        json_ext = {
            "location": location,
            "sign": sign,
            "lat": lat,
            "lng": lng,
        }
        u.ext = json_ext
        u.banner = params.get('banner', u.banner)
        u.last_upload = params.get('last_upload', u.last_upload)
        db.session.commit()
        return u

    @classmethod
    def get_similar_users(cls, user_id):
        sql = """
            SELECT id AS user_id,name,portrait,gender FROM user WHERE id IN (
              SELECT distinct user_id from action WHERE res_id IN (
              SELECT res_id FROM action WHERE type = 27 AND user_id = %s
            ) AND user_id>''
            );
        """

        return query(sql, [user_id])


class UserOpen(BaseBean, db.Model):
    __tablename__ = 'user_open'
    id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), default="")
    name = db.Column(db.String)
    portrait = db.Column(db.String)
    location = db.Column(db.String)
    source = db.Column(db.String)
    gender = db.Column(db.Float)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_items(cls, **params):
        return UserOpen.query.filter_by(**params).all()

    @classmethod
    def query_open_user(cls, **params):
        return UserOpen.query.filter_by(**params).first()

    @classmethod
    def update_open_user_by_id(cls, id, **params):
        uo = cls.query.get(id)
        uo.user_id = params.get('user_id', uo.user_id)

        db.session.commit()
        return uo

    @classmethod
    def create_open_user_and_user(cls, **params):
        if 'open_id' in params:
            params['id'] = params['open_id']
            del params['open_id']
        open_user = UserOpen(**params)
        user = User.create_user(
            name=params.get('name'),
            portrait=params.get('portrait')
        )
        open_user.user_id = user.id

        db.session.add(open_user)
        db.session.commit()
        return open_user

    @classmethod
    def create_open_user(cls, **params):
        if 'open_id' in params:
            params['id'] = params['open_id']
            del params['open_id']
        open_user = UserOpen(**params)

        db.session.add(open_user)
        db.session.commit()
        return open_user


class UserAttention(BaseBean, db.Model):
    __tablename__ = 'user_attention'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    user_id = db.Column(db.String)
    to_user_id = db.Column(db.BIGINT)
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def query_user_attention(cls, **params):
        if params:
            params['is_del'] = 0
        return UserAttention.query.filter_by(**params).first()

    @classmethod
    def query_user_attentions(cls, **params):
        if params:
            params['is_del'] = 0
        return UserAttention.query.filter_by(**params).all()

    @classmethod
    def query_user_attention_paginate(cls, page, per_page, **params):
        if params:
            params['is_del'] = 0

        return UserAttention.query.filter_by(**params).order_by(
            desc(UserAttention.create_ts)).paginate(page, per_page, False)


@query_params('user_id')
def update_open_user_by_id(open_id, params=None):
    uo = UserOpen.query.get(open_id)
    uo.user_id = get_param(params, 'user_id', uo.user_id)

    res = db.session.commit()

    print(res)
    return uo


def create_and_binding_open_user(user_id, params):
    '''绑定第三方用户'''
    name = params['name']
    open_id = params['open_id']
    source = params['source']
    portrait = params['portrait']
    gender = params['gender']
    location = params['location']
    ou = UserOpen(
        id=open_id,
        source=source,
        name=name,
        user_id=user_id,
        portrait=portrait,
        gender=gender,
        location=location,
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(ou)
    db.session.commit()
    return ou


def binding_open_user(open_id, user_id):
    '''绑定第三方用户'''
    uo = UserOpen.query.get(open_id)
    uo.user_id = user_id
    db.session.commit()
    return uo


def unbinding_open_user(open_id, user_id=None):
    '''绑定第三方用户'''
    uo = UserOpen.query.get(open_id)

    uo.user_id = 0
    db.session.commit()
    return uo


def create_open_user(params):
    '''常见第三方用户'''
    name = params['name']
    user = create_user(
        name=name,
        status=BaseConfig.TYPE_USER_NORMAL
    )

    return create_and_binding_open_user(user.id, params)


def query_open_user_by_id(id):
    '''通过id过去第三方用户'''
    return UserOpen.query.get(id)


def on_attontion(**params):
    '''关注'''
    off_attontion(**params)
    ua = UserAttention(
        user_id=params['user_id'],
        to_user_id=params['to_user_id'],
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(ua)
    db.session.commit()


def off_attontion(**params):
    '''取消关注'''
    sql = 'update user_attention set is_del = 1 ' \
          'WHERE user_id = :user_id and to_user_id = :to_user_id'
    db.engine.execute(text(sql), user_id=params['user_id'],
                      to_user_id=params['to_user_id'])


def query_user_attention(user_id, to_user_id):
    """获取用户关注状态"""
    return UserAttention.query.filter_by(
        user_id=user_id,
        to_user_id=to_user_id,
        is_del=0
    ).first()


def query_user_by_id(user_id):
    '''根据id查询用户'''
    return User.query.filter_by(id=user_id, is_del=0).first()


@query_params('with_opens')
def make_user_by_id(user_id, params=None):
    '''根据user_id生成用户对象'''
    user = query_user_by_id(user_id)

    if not user:
        return None
    item = user.to_json()

    item['create_ts'] = utils.make_timestamp_for_sql_time(item['create_ts'])
    item['user_id'] = item['id']

    del item['update_ts']
    del item['id']
    del item['is_del']

    # 查找第三方用户
    with_opens = get_param(params, 'with_opens', True)
    if with_opens:
        opens = []
        for open_user in user.opens:
            opens.append({
                "open_id": open_user.id,
                "source": open_user.source
            })
        item['opens'] = opens

    return item


def query_user_by_mobile(mobile):
    return User.query.filter_by(mobile=mobile, is_del=0).first()


def update_user_by_id(user_id, **params):
    '''根据用户id修改信息'''
    u = User.query.filter_by(id=user_id).first()
    u.name = get_param(params, 'name', u.name)
    u.mobile = get_param(params, 'mobile', u.mobile)
    u.portrait = get_param(params, 'portrait', u.portrait)
    u.gender = get_param(params, 'gender', u.gender)
    u.age = get_param(params, 'age', u.age)
    u.status = get_param(params, 'status', u.status)

    ext = u.ext
    print(ext)
    location = get_param(params, 'location', ext['location'])
    sign = get_param(params, 'sign', ext['sign'])
    sign = get_param(params, 'sign', ext['sign'])
    lat = get_param(params, 'lat', ext['lat'])
    lng = get_param(params, 'lng', ext['lng'])

    json_ext = {
        "location": location,
        "sign": sign,
        "lat": lat,
        "lng": lng,
    }
    u.ext = json_ext
    db.session.commit()
    return u


# def create_anonymous_user():
#     '''创建匿名用户'''
#     name = '匿名{}'.format(utils.get_random_num(5))
#     return create_user(name=name)


def create_user(**params):
    '''创建用户'''
    mobile = get_param(params, 'mobile', '')
    name = get_param(params, 'name', '')
    status = get_param(params, 'status', BaseConfig.DEFAULT_USER_STATUS)
    new_id = snowflake.generate()

    ext = {
        "location": "",
        "sign": "",
        "lat": 0,
        "lng": 0
    }

    u = User(
        id=new_id,
        mobile=mobile,
        name=name,
        portrait=BaseConfig.DEFAULT_PORTRAIT,
        age=BaseConfig.DEFAULT_AGE,
        gender=BaseConfig.DEFAULT_GENDER,
        status=status,
        ext=ext,
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(u)
    db.session.commit()
    return u
