#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''启动定时任务程序'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src import app
from src.api.video import models as  video_db
from src.common import pymysql_util as db
from src.config import BaseConfig
from src.common.letv import video_client
from src.common.letv import constants as LETV

from apscheduler.schedulers.background import BackgroundScheduler


def check_video_status():
    try:


        res = video_db.query_video_list(
            status=BaseConfig.TYPE_VIDEO_STATUS_TRANSCODING
        )
        for item in res:
            video_id = item.id
            video_detail = video_client.get_video(item.ext['letv_video_id'])
            if video_detail:
                status = int(video_detail['status'])
                print(video_id, status)
                if status == LETV.VIDEO_STATUS_NORMAL:
                    video_db.update_video(
                        video_id=video_id,
                        status=BaseConfig.TYPE_VIDEO_STATUS_NORMAL)

    except BaseException as e:
        print(e)


sched = BackgroundScheduler()
sched.add_job(check_video_status, 'interval', seconds=2)
# sched.add_job(sync_collection_movie(), 'interval', seconds=5)
# sched.add_job(sync_collection_show(), 'interval', seconds=5)
# sched.add_job(my_job, 'interval', seconds=5)
# sched.add_job(my_job1, 'interval', seconds=5)
sched.start()
