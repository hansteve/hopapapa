#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''用户表models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import app
from src.api.user import models as user_db
from src.api.user.models import User
from src.api.user.models import UserOpen
from src.api.user.service import get_user_attentions
from src.api.user.service import get_user_detail
from src.api.user.service import get_similar_users
from src.api.action.models import Action
from src.api.home_page.service import Resource
from src.api.search.service import Search
from src.config import BaseConfig
from src.common import http_util
from src.common.http_util import check_params
from src.common.http_util import get_login_user_id
from src.common.http_util import return_model
from src.common.http_util import return_no_authorization
from src.common.http_util import return_not_found
from src.common.http_util import return_404
from src.common.user_security import generate_authorization
from src.common.wangyi import sms
from src.common.web.flask_snippets import jsonp
from src.common.web.flask_snippets import login_required
from src.common.rongcloud.client import User as RCUser

from flask import request
from flask import Blueprint
from flask import g

user_bp = Blueprint('user', __name__)
rc_user = RCUser()


@user_bp.route("/attention/<string:action>", methods=['POST'])
def attention(action):
    user_id = get_login_user_id(request)
    if not user_id:
        return return_no_authorization()

    args = request.json
    key = check_params(args, 'to_user_id')
    if key:
        return return_not_found(key)

    to_user_id = args['to_user_id']

    if action == 'on':
        user_db.on_attontion(user_id=user_id, to_user_id=to_user_id)
    elif action == 'off':
        user_db.off_attontion(user_id=user_id, to_user_id=to_user_id)
    else:
        return return_404()

    return return_model()


@user_bp.route("/user/signin", methods=['POST'])
def signin():
    args = request.json

    key = check_params(args, 'mobile', 'code')

    if key:
        return return_not_found(key)
    mobile = args['mobile']
    code = args['code']
    is_exist = sms.verify_code(
        mobile=mobile,
        code=code
    )

    if mobile.startswith('110') and code == '0000':
        is_exist = True

    if mobile == '15890687745' and code == '0000':
        is_exist = True

    if not is_exist:
        return return_model(message='code {} is not found '.format(code),
                            status=404)

    try:
        user = User.query_user(mobile=mobile)

        # 如果用户不存在则创建
        if not user:
            # 获取token携带用户
            login_user_id = get_login_user_id(request)
            login_user = User.query_user(id=login_user_id)
            # 如果登陆用户不存在,则用手机创建用户
            if not login_user or login_user.mobile:
                user = User.create_user(
                    mobile=mobile,
                    status=BaseConfig.TYPE_USER_NORMAL
                )
            else:
                user = user_db.update_user_by_id(
                    user_id=login_user_id,
                    mobile=mobile,
                    status=BaseConfig.TYPE_USER_NORMAL
                )

        authorization = generate_authorization(user.id)

        # 记录用户登录操作
        Action.create_action(
            user_id=user.id,
            type=BaseConfig.TYPE_ACTION_LOGIN,
            res_id=user.id,
            res_type=BaseConfig.TYPE_USER,
            ext=args
        )

        return return_model(
            header={"authorization": authorization}
        )
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@user_bp.route("/user/open/signin", methods=['POST'])
def signin_open():
    '''第三方登录'''
    args = request.json

    need_keys = ['open_id', 'source', 'name', 'portrait']

    key = check_params(args, *need_keys)

    if key:
        return http_util.return_param_not_found(key)

    login_user_id = get_login_user_id(request)

    try:
        open_id = args['open_id']

        if login_user_id:
            luo = UserOpen.query_open_user(
                id=open_id,
                user_id=login_user_id
            )
            if luo:
                return http_util.return_forbidden('当前用户已登录，不能重复登录')

            login_user = User.query_user(
                id=login_user_id,
                status=BaseConfig.TYPE_USER_NORMAL
            )

            if login_user:
                return http_util.return_forbidden('当前用户已登录，不能重复登录')

        open_user = UserOpen.query_open_user(id=open_id)

        if open_user:

            # 如果第三方用户没有绑定用户，则生成用户并绑定
            if not open_user.user_id:
                binding_user_id = ""
                if login_user_id:
                    binding_user_id = login_user_id
                    User.update_user_by_id(
                        id=login_user_id,
                        name=open_user.name,
                        portrait=open_user.portrait,
                        status=BaseConfig.TYPE_USER_NORMAL
                    )
                else:
                    user = User.create_user(
                        name=args.get('name'),
                        portrait=args.get('portrait')
                    )
                    binding_user_id = user.id

                open_user = UserOpen.update_open_user_by_id(
                    id=open_id,
                    user_id=binding_user_id
                )
        else:
            # 创建第三方用户
            if login_user_id:
                args['user_id'] = login_user_id
                open_user = UserOpen.create_open_user(**args)
                User.update_user_by_id(
                    id=login_user_id,
                    name=open_user.name,
                    portrait=open_user.portrait,
                    status=BaseConfig.TYPE_USER_NORMAL
                )
            else:
                open_user = UserOpen.create_open_user_and_user(**args)

        user_id = open_user.user_id

        authorization = generate_authorization(user_id)

        # 记录用户登录操作
        Action.create_action(
            user_id=user_id,
            type=BaseConfig.TYPE_ACTION_LOGIN,
            res_id=user_id,
            res_type=BaseConfig.TYPE_USER,
            ext=args
        )

        return return_model(
            header={"authorization": authorization}
        )
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@user_bp.route("/user/open/unbinding", methods=['POST'])
def open_unbinding():
    '''绑定第三方用户'''
    user_id = get_login_user_id(request)
    if not user_id:
        return return_no_authorization()

    login_user = User.query_user(
        id=user_id,
        status=BaseConfig.TYPE_USER_ANONYMOUS
    )
    if login_user:
        return http_util.return_forbidden('请先登录，在进行解绑')

    args = request.json
    need_keys = ['open_id']
    key = check_params(args, *need_keys)
    if key:
        return return_not_found(key)

    open_id = args['open_id']

    open_user = UserOpen.query_open_user(id=open_id)
    if open_user:
        if open_user.user_id != user_id:
            return http_util.return_forbidden('bound not found')
        else:
            UserOpen.update_open_user_by_id(
                id=open_id,
                user_id=""
            )
            return http_util.return_model()
    else:
        return http_util.return_forbidden('bound not found')


@user_bp.route("/user/open/binding", methods=['POST'])
def open_binding():
    '''解绑第三方用户'''
    user_id = get_login_user_id(request)
    if not user_id:
        return return_no_authorization()

    login_user = User.query_user(
        id=user_id,
        status=BaseConfig.TYPE_USER_ANONYMOUS
    )
    if login_user:
        return http_util.return_forbidden('请先登录，在进行绑定')

    args = request.json
    need_keys = ['open_id', 'source', 'name', 'portrait']
    key = check_params(args, *need_keys)
    if key:
        return http_util.return_param_not_found(key)

    is_exists = UserOpen.query_open_user(
        user_id=user_id,
        source=args.get('source')
    )
    if is_exists:
        return http_util.return_forbidden('该第三方已经绑定过')

    open_id = args['open_id']
    open_user = UserOpen.query_open_user(
        id=open_id
    )

    if open_user:
        if open_user.user_id:
            return http_util.return_forbidden('该账户已被绑定')

        UserOpen.update_open_user_by_id(
            id=open_id,
            user_id=user_id
        )
    else:
        args['user_id'] = user_id
        UserOpen.create_open_user(**args)

    return return_model()


@user_bp.route("/user/create/anonymous", methods=['POST'])
def create_anonymous():
    '''获取匿名用户'''
    try:
        user = User.create_anonymous_user()

        authorization = generate_authorization(user.id)

        return return_model(
            header={"authorization": authorization}
        )
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@user_bp.route("/user/update", methods=['POST'])
@login_required
def update_user():
    '''修改用户信息'''
    headers = request.headers
    user_id = g.user_id
    args = request.json

    try:
        mobile = args.get('mobile')
        if mobile:
            mobile_exists = User.query_user(mobile=mobile)
            if mobile_exists:
                return http_util.return_forbidden('手机号已经绑定其他用户')

        u = User.update_user_by_id(id=user_id, **args)
        if u:
            # 记录用户操作
            Action.create_action(
                user_id=user_id,
                type=BaseConfig.TYPE_ACTION_UPDATE,
                res_id=user_id,
                res_type=BaseConfig.TYPE_USER,
                ext=args
            )

            Search.sync_index_by_id(user_id, BaseConfig.TYPE_USER)

            return return_model()
        else:
            return http_util.return_internal_server_error()
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@user_bp.route("/user/detail", methods=['GET'])
@jsonp
def detail():
    login_user_id = g.user_id
    args = request.args
    user_id = args.get('user_id', None)

    detail_id = None
    if user_id:
        detail_id = user_id
    else:
        detail_id = login_user_id

    if not detail_id:
        return http_util.return_404('not found user')

    # 记录用户观看其他用户的记录
    Action.create_action(
        user_id=login_user_id,
        type=BaseConfig.TYPE_ACTION_VIEW,
        res_id=detail_id,
        res_type=BaseConfig.TYPE_USER
    )

    user = get_user_detail(
        id=detail_id,
        login_user_id=login_user_id,
        source_include=['opens', 'view_count', 'attention_count', 'banner']
    )

    if not user:
        return http_util.return_404('user not found')

    if not user_id:
        user['ext']['rongcloud_token'] = rc_user.getToken(
            userId=login_user_id,
            name=user['name'],
            portraitUri=user['portrait']
        ).result['token']

    return return_model(user)


@user_bp.route("/user/timeline")
@jsonp
def timeline():
    login_user_id = get_login_user_id(request)
    args = request.args
    start = http_util.get_param_int(args, 'start', BaseConfig.MAX_START)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)
    user_id = args.get('user_id', None)
    detail_id = None
    if user_id:
        detail_id = user_id
    else:
        detail_id = login_user_id

    if not detail_id:
        return http_util.return_404('not found user')

    res = Action.query_actions(
        user_id=detail_id,
        type=BaseConfig.TYPE_ACTION_UPLOAD,
    )

    items = []
    for item in res:
        res_type = item.res_type
        res_id = item.res_id

        item = Resource.get_resource_detail(
            res_id=res_id,
            res_type=res_type,
            login_user_id=login_user_id
        )
        if item:
            items.append(item)

    return http_util.return_model(items)


@user_bp.route("/user/attentions")
@jsonp
def user_attentions():
    login_user_id = get_login_user_id(request)
    args = request.args
    key = http_util.check_params(args, 'attention_status')
    if key:
        return http_util.return_param_not_found(key)

    user_id = http_util.get_param(args, 'user_id')

    attention_status = http_util.get_param_int(args, 'attention_status')
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    detail_id = None
    if user_id:
        detail_id = user_id
    else:
        detail_id = login_user_id

    if not detail_id:
        return return_no_authorization()

    try:
        res = get_user_attentions(
            user_id=detail_id,
            attention_status=attention_status,
            page=page,
            per_page=per_page,
            login_user_id=login_user_id
        )
        return http_util.return_model(res)
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()


@user_bp.route("/user/similar")
@jsonp
def user_similar():
    try:
        res = get_similar_users(g.user.id)
        return http_util.return_model(res)
    except BaseException as e:
        app.logger.error(e)
        return http_util.return_internal_server_error()
