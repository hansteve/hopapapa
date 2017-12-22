#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''pymysql工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import logging

import pymysql.cursors
from src import env_config
from urlparse import urlparse

URL_CONFIG = urlparse(env_config.SQLALCHEMY_DATABASE_URI)


def create_conn():
    '''创建数据库连接'''
    return pymysql.connect(
        host=URL_CONFIG.hostname,
        port=URL_CONFIG.port,
        user=URL_CONFIG.username,
        password=URL_CONFIG.password,
        db=URL_CONFIG.path[1:],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def query(sql, params):
    """
    查询操作
    :param sql:
    :param params:
    :return:
    """
    conn = create_conn()
    try:
        cursor = conn.cursor()

        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except BaseException as e:
        logging.error(e)
        return []
    finally:
        conn.close()


def execute(sql, params):
    """
    更新操作
    :param sql:
    :param params:
    :return:
    """
    conn = create_conn()
    try:
        cursor = conn.cursor()

        result = cursor.execute(sql, params)
        conn.commit()
        cursor.close()
        return result
    except BaseException as e:
        logging.error(e)
        return False
    finally:
        conn.close()
