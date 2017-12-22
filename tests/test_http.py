#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''搜索api程序'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time
import requests

from src.config import BaseConfig
from src.common.utils import get_random_num
from src.api.user import models as user_db
from src.api.location.models import create_location
from src.api.location.models import query_user_last_location
from src import db
from sqlalchemy import text
from src.common.pymysql_util import execute

from src.api.code.models import Code
from tests.test_snowflake import Snowflake

import requests

if __name__ == '__main__':
    url = 'http://localhost:8000/api/v1/location/create'

    locals = [
        {'lat': 39.9147520000, 'lng': 116.4041450000},
        {'lat': 39.9147520000, 'lng': 116.4041460000},
        {'lat': 39.9147520000, 'lng': 116.4041470000},
        {'lat': 39.9147520000, 'lng': 116.4041480000},
        {'lat': 39.9147520000, 'lng': 116.4041490000},
        {'lat': 39.9147530000, 'lng': 116.4041490000},
        {'lat': 39.9147540000, 'lng': 116.4041490000},
        {'lat': 39.9147550000, 'lng': 116.4041490000},
        {'lat': 39.9147560000, 'lng': 116.4041490000},
        {'lat': 39.9147570000, 'lng': 116.4041490000},
        {'lat': 39.9147580000, 'lng': 116.4041490000},
        {'lat': 39.9147520000, 'lng': 116.4041400000}
    ]

    url = "http://api.map.baidu.com/geodata/v3/poi/create"

    for local in locals:
        payload = {
            "latitude": local['lat'],
            "longitude": local['lng'],
            "ak": BaseConfig.BAIDU_MAP_AK,
            "coord_type": 3,
            "geotable_id": 165640,
            "user_id": get_random_num(6)
        }
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
        }

        response = requests.post(url, data=payload, headers=headers)

        print(response.json())
