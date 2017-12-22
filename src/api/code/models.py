#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''code表models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import db
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.utils import get_random_num


class Code(BaseBean, db.Model):
    __tablename__ = 'code'
    id = db.Column(db.BIGINT, primary_key=True, unique=True)
    mobile = db.Column(db.String)
    code = db.Column(db.String)
    is_del = db.Column(db.Integer)
    create_ts = db.Column(db.TIMESTAMP)


def create_code_by_mobile(mobile):
    '''创建短信验证码'''
    code = get_random_num(6)
    c = Code(
        mobile=mobile,
        code=code,
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(c)
    db.session.commit()
    return c


def query_code(**params):
    return Code.query.filter_by(mobile=params['mobile'], code=params['code'],
                                is_del=0).first()
