#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''评论表models'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."


from src import db
from src import snowflake
from src.config import BaseConfig
from src.common.base import BaseBean
from src.common.pymysql_util import query



class Comment(BaseBean, db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String)
    to_user_id = db.Column(db.String)
    res_id = db.Column(db.String)
    res_type = db.Column(db.Integer)
    content = db.Column(db.String)
    is_del = db.Column(db.Integer, default=0)
    create_ts = db.Column(db.TIMESTAMP)
    update_ts = db.Column(db.TIMESTAMP)

    @classmethod
    def get_comments(cls, **params):
        '''获取评论列表'''
        start = int(params['start'])
        res_id = params['res_id']
        per_page = int(params['per_page'])

        sql = "select * from view_comment WHERE res_id = %s " \
              "and create_ts < %s limit 0,%s;"
        res = query(sql, [res_id, start, per_page])
        return res

    @classmethod
    def get_replys(cls, **params):
        '''根据评论id过去回复列表'''
        comment_id = params['comment_id']
        sql = ' select * from view_reply where comment_id = %s'
        res = query(sql, [comment_id])
        return res

    @classmethod
    def query_count(cls, **params):
        if params:
            params['is_del'] = 0

        return Comment.query.filter_by(**params).count()


def create_comment(**keywords):
    '''创建评论'''
    new_id = snowflake.generate()
    c = Comment(
        id=new_id,
        user_id=keywords['user_id'],
        to_user_id="",
        res_id=keywords['res_id'],
        res_type=BaseConfig.TYPE_RES,
        content=keywords['content'],
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(c)
    db.session.commit()
    return c


def create_reply(**params):
    '''创建回复'''
    new_id = snowflake.generate()
    c = Comment(
        id=new_id,
        user_id=params['user_id'],
        to_user_id=params['to_user_id'],
        res_id=params['comment_id'],
        res_type=BaseConfig.TYPE_COMMENT,
        content=params['content'],
        is_del=BaseConfig.DEFAULT_IS_DEL
    )
    db.session.add(c)
    db.session.commit()
    return c


#
# def get_comments(**params):
#     '''获取评论列表'''
#     start = int(params['start'])
#     res_id = params['res_id']
#     sql = QUERY_PREFIX + ' and res_id = %s and create_ts < %s  ' \
#                          'order by create_ts desc;'
#     t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
#     res = query(sql, [res_id, t])
#     map(loop_comments, res)
#     return res


# def get_replys_by_comment_id(comment_id):
#     '''根据评论id过去回复列表'''
#     sql = ' select * from view_comment where   res_id = %s and res_type = %s'
#
#     res = query(sql, [comment_id, BaseConfig.TYPE_COMMENT])
#     map(loop_comments, res)
#     return res
#
#
# def loop_comments(item):
#     '''制作评论列表'''
#     # 构造用户信息
#     user_id = item['user_id']
#     item['from_user'] = make_comment_user(user_id)
#     del item['user_id']
#
#     # 构造回复
#     res_type = item['res_type']
#     comment_id = item['comment_id']
#     if res_type == BaseConfig.TYPE_RES:
#         replys = get_replys_by_comment_id(comment_id)
#         if replys:
#             item['replys'] = replys
#     elif res_type == BaseConfig.TYPE_COMMENT:
#         item['reply_id'] = comment_id
#         del item['comment_id']
#
#         to_user_id = item['to_user_id']
#         to_user = make_comment_user(to_user_id)
#         item['to_user'] = to_user
#
#     del item['res_type']
#     del item['to_user_id']


# def make_comment_user(user_id):
#     return utils.filter_json(make_user_by_id(user_id, with_opens=False),
#                              source_include=['user_id', 'portrait', 'name'])
