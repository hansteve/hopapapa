#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video views'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common import http_util
from src.config import BaseConfig
from src.api.collection.models import Collection
from src.api.collection.models import CollectionResource
from src.api.home_page.service import Resource
from src.common.http_util import return_model
from src.common.web.flask_snippets import crossdomain
from src.common.web.flask_snippets import jsonp

from flask import request
from flask import Blueprint

admin_collection_bp = Blueprint('admin_collection', __name__)


@admin_collection_bp.route('/collection/list.json', methods=['GET'])
@jsonp
def list():
    '''首页列表'''
    args = request.args
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = Collection.query_paginate(
        page=page,
        per_page=per_page
    )

    details = []
    for item in paginate.items:
        detail = item.to_json()
        # res_type = detail['res_type']
        # res_id = detail['res_id']
        # res_detail = Resource.get_resource_detail(
        #     res_id=res_id,
        #     res_type=res_type
        # )
        # detail['res_detail'] = res_detail
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_collection_bp.route('/collection/sub/list.json', methods=['GET'])
@jsonp
def sub_list():
    '''首页列表'''
    args = request.args
    page = http_util.get_param_int(args, 'page', BaseConfig.DEFAULT_PAGE)
    per_page = http_util.get_param_int(args, 'per_page',
                                       BaseConfig.DEFAULT_PER_PAGE)

    paginate = CollectionResource.query_paginate(
        page=page,
        per_page=per_page,
        collection_id=args.get('collection_id', '')
    )

    details = []
    for item in paginate.items:
        detail = item.to_json()
        res_type = detail['res_type']
        res_id = detail['res_id']
        res_detail = Resource.get_resource_detail(
            res_id=res_id,
            res_type=res_type
        )
        detail['res_detail'] = res_detail
        print(res_detail)
        details.append(detail)

    res = http_util.make_page_response(details, paginate.total, page,
                                       per_page)

    return return_model(
        data=res
    )


@admin_collection_bp.route('/collection/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def edit_json():
    """创建或修改首页信息"""
    args = request.form
    id = args.get('id', None)

    if id:
        Collection.update_by_id(**args)
    else:
        Collection.create(**args)

    return return_model()


@admin_collection_bp.route('/collection/sub/edit.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def sub_edit_json():
    """创建或修改首页信息"""
    args = request.form
    id = args.get('id', None)

    if id:
        CollectionResource.update_by_id(**args)
    else:
        CollectionResource.create(**args)

    return return_model()


@admin_collection_bp.route('/collection/sub/delete.json', methods=['POST'])
@crossdomain(origin='*', methods=['POST'], headers='Origin, Content-Type')
def sub_delete_json():
    """创建或修改首页信息"""
    args = request.form
    id = args.get('id', None)

    CollectionResource.delete(
        id=id
    )

    return return_model()
