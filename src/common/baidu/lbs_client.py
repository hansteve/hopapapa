#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''视频逻辑模块'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import sys
import requests

from src import app
from src.config import BaseConfig
from src.common import http_util
from src.common.letv import video_client

from elasticsearch.client import query_params
from flask import request

reload(sys)
sys.setdefaultencoding('utf8')


def create_geotable(table_name):
    '''创建geotable表'''
    data = {
        'ak': BaseConfig.BAIDU_MAP_AK,
        'is_published': 1,
        'geotype': 1,
        'name': table_name
    }

    res = requests.post(
        url='http://api.map.baidu.com/geodata/v3/geotable/create',
        data=data
    )

    data = res.json()

    status = data['status']
    if status == 0:
        return status, data['id']
    else:
        return status, data['message']


def create_poi(geo_id, lat, lng, **params):
    '''创建poi'''
    data = {
        'latitude': lat,
        'ak': BaseConfig.BAIDU_MAP_AK,
        'longitude': lng,
        'coord_type': '3',
        'geotable_id': geo_id
    }

    if params:
        for key, value in params.iteritems():
            data[key] = value

    res = requests.post(
        url='http://api.map.baidu.com/geodata/v3/poi/create',
        data=data
    )

    data = res.json()

    status = data['status']

    if status == 0:
        return status, data['id']
    else:
        app.logger.error(data['message'])
        return status, data['message']

@query_params('user_id')
def delete_poi(geo_id, params=None):
    '''删除poi'''
    data = {
        'ak': BaseConfig.BAIDU_MAP_AK,
        'geotable_id': geo_id
    }
    if params:
        for key, value in params.iteritems():
            data[key] = value

    res = requests.post(
        url='http://api.map.baidu.com/geodata/v3/poi/delete',
        data=data
    )

    data = res.json()

    status = data['status']

    if status == 0:
        return status, data['id']
    else:
        return status, data['message']


@query_params('tags', 'page_index', 'page_size')
def search_near(geo_id, lat, lng, radius=1000, params=None):
    '''搜索附近的坐标'''
    data = {
        'ak': BaseConfig.BAIDU_MAP_AK,
        'geotable_id': geo_id,
        'location': '{},{}'.format(lng, lat),
        'radius': radius,
        'sortby': 'status:-1|distance:1'
    }
    if params:
        for key, value in params.iteritems():
            data[key] = value

    res = requests.get(
        url='http://api.map.baidu.com/geosearch/v3/nearby',
        params=data
    )

    data = res.json()
    status = data['status']

    print(data)

    if status == 0:
        return data['contents'], data['total']
    else:
        return [], 0


if __name__ == '__main__':
    status, data = create_geotable('geo_dev')
    #   165639    geo_prod
    #   165640      geo_dev

    print(status, data)
