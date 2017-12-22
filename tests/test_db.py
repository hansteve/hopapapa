#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''搜索api程序'''
from sqlalchemy import desc

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import time
import requests

from src.config import BaseConfig
from src.api.action.models import Action
from src.api.audio.models import Audio
from src.api.user.models import User
from src.api.user.models import UserOpen
from src.api.user.service import get_user_detail
from src.api.user.service import get_user_detail
from src.api.video import models as video_db
from src.api.video.models import Video
from src.api.article.models import Article
from src.api.location.models import create_location
from src.api.location.models import query_user_last_location
from src.api.home_page.models import ViewHotRes
from src import db
from sqlalchemy import text
from src.common.pymysql_util import execute
from src.common import utils

from src.api.code.models import Code
from src.api.collection.models import CollectionResource
from tests.test_snowflake import Snowflake
from src.common.aliyun_util import put_object

if __name__ == '__main__':


    items = Article.query_articles(
        is_del=0
    )
    for item in items:
        poster = item.poster
        print(poster)
        try:
            res = requests.get(poster)
            print(res)
            if res.status_code == 200:
                suffix = poster.rsplit('.', 1)[1]
                datetime_root = time.strftime("%Y%m%d/%H/%M%S", time.localtime())
                url = put_object(
                    key='{}/{}.{}'.format(datetime_root, int(time.time()), suffix),
                    data=res.content,
                    bucket_name=BaseConfig.ALIYUN_BUCKET_IMG
                )
                Article.update_article_by_id(
                    id=item.id,
                    poster=url
                )
                print(url)
        except BaseException as e:
            print(e)
        pass



def sync_audio_poster():
    items = Audio.query_audios(
        is_del=0
    )
    for item in items:
        poster = item.poster
        print(poster)
        try:
            res = requests.get(poster)
            print(res)
            if res.status_code == 200:
                suffix = poster.rsplit('.', 1)[1]
                datetime_root = time.strftime("%Y%m%d/%H/%M%S",
                                              time.localtime())
                url = put_object(
                    key='{}/{}.{}'.format(datetime_root, int(time.time()),
                                          suffix),
                    data=res.content,
                    bucket_name=BaseConfig.ALIYUN_BUCKET_IMG
                )
                Audio.update_audio_by_id(
                    id=item.id,
                    poster=url
                )
                print(url)
        except BaseException as e:
            print(e)


def sync_video_poster():
    items = Video.query_videos(
        is_del=0
    )
    for item in items:
        poster = item.poster
        print(poster)
        try:
            res = requests.get(poster)
            print(res)
            if res.status_code == 200:
                suffix = poster.rsplit('.', 1)[1]
                datetime_root = time.strftime("%Y%m%d/%H/%M%S",
                                              time.localtime())
                url = put_object(
                    key='{}/{}.{}'.format(datetime_root, int(time.time()),
                                          suffix),
                    data=res.content,
                    bucket_name=BaseConfig.ALIYUN_BUCKET_IMG
                )
                Video.update_video_by_id(
                    id=item.id,
                    poster=url
                )
                print(url)
        except BaseException as e:
            print(e)
