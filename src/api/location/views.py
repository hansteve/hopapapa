#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''location表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import env_config
from src.config import BaseConfig
from src.api.location import models
from src.api.user import models as user_db
from src.api.user.models import User
from src.api.user.service import get_user_detail
from src.api.action.models import Action
from src.api.home_page.service import Resource
from src.common import http_util
from src.common.baidu.lbs_client import create_poi
from src.common.baidu.lbs_client import delete_poi
from src.common.baidu.lbs_client import search_near
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

location_bp = Blueprint('location', __name__)


@location_bp.route('/location/create', methods=['POST'])
def create_location():
    '''创建坐标'''
    user_id = http_util.get_login_user_id(request)
    if not user_id:
        return http_util.return_no_authorization()
    args = request.json
    key = http_util.check_params(args, 'lat', 'lng')
    if key:
        return http_util.return_param_not_found(key)

    user = User.query_user(id=user_id)
    if not user:
        return http_util.return_forbidden("this user_id can't found user ")

    lat = args['lat']
    lng = args['lng']
    la = models.create_location(
        user_id=user_id,
        lat=lat,
        lng=lng
    )

    delete_poi(
        geo_id=env_config.GEOTABLE_ID,
        user_id=user_id
    )
    create_poi(
        geo_id=env_config.GEOTABLE_ID,
        lat=lat,
        lng=lng,
        user_id=user_id,
        status=user.status
    )

    User.update_user_by_id(
        id=user_id,
        lat=lat,
        lng=lng
    )

    if la:
        return http_util.return_model()
    else:
        return http_util.return_internal_server_error()


@location_bp.route('/location/near', methods=['GET'])
@jsonp
def near():
    '''附近坐标'''
    login_user_id = http_util.get_login_user_id(request)
    if not login_user_id:
        return http_util.return_no_authorization()
    args = request.args
    page_size = http_util.get_param_int(args, 'per_page', 50)
    key = http_util.check_params(args, 'radius', 'lat', 'lng')
    if key:
        return http_util.return_param_not_found(key)

    lat = http_util.get_param(args, 'lat')
    lng = http_util.get_param(args, 'lng')
    radius = http_util.get_param_int(args, 'radius', 1000)
    items, total = search_near(
        geo_id=env_config.GEOTABLE_ID,
        lat=lat,
        lng=lng,
        radius=radius,
        page_size=50
    )

    users = []
    for item in items:
        user_id = item['user_id']
        location = item['location']
        lat = location[1]
        lng = location[0]
        user = get_user_detail(id=user_id)

        if not user:
            continue
        user['ext']['lat'] = lat
        user['ext']['lng'] = lng
        if login_user_id != user_id:
            users.append(user)

    res = http_util.make_page_response(users, total, 1, page_size)

    return http_util.return_model(
        data=res
    )
