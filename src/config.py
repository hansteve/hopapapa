#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''配置信息'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."


class BaseConfig(object):
    DEBUG = False

    ES_INDEX = 'hopapapa'

    ES_TYPE_USER = 'user'
    ES_TYPE_VIDEO = 'video'
    ES_TYPE_ARTICLE = 'article'
    ES_TYPE_AUDIO = 'audio'
    ES_TYPE_COLLECTION = 'collection'

    ES_PARAMS_WEIGHT = 'es_weight'

    ES_WEIGHT_USER = 10000
    ES_WEIGHT_COLLECTION = 9000
    ES_WEIGHT_VIDEO = 8000
    ES_WEIGHT_AUDIO = 8000
    ES_WEIGHT_ARTICLE = 7000

    TYPE_USER = 1  # 用户
    TYPE_RES = 2  # 资源
    TYPE_COMMENT = 3  # 评论
    TYPE_IMAGE = 4  # 图片
    TYPE_ARTICLE = 6  # 文章
    TYPE_VIDEO_PLAY = 7  # 视频点播
    TYPE_VIDEO_LIVE = 8  # 视频直播
    TYPE_AUDIO = 11  # 音频
    TYPE_COLLECTION = 12  # 集合
    TYPE_PUSH = 13  # 推送
    TYPE_ACTION_DELETE = 21  # 删除
    TYPE_ACTION_LOGIN = 22  # 登录
    TYPE_ACTION_UPDATE = 23  # 修改用户信息
    TYPE_ACTION_VIEW_HOME_PAGE_SHOW = 24  # 观看弹框
    TYPE_ACTION_VIEW = 27  # 观看
    TYPE_ACTION_UPLOAD = 28  # 上传
    TYPE_USER_ANONYMOUS = 51  # 匿名用户
    TYPE_USER_NORMAL = 52  # 正常用户
    TYPE_VIDEO_STATUS_NORMAL = 71  # 正常
    TYPE_VIDEO_STATUS_TRANSCODING = 72  # 转码中
    TYPE_HOME_PAGE_CAROUSEL = 81  # 首页轮播图
    TYPE_HOME_PAGE_LIST = 82  # 首页列表
    TYPE_HOME_PAGE = 83  # 首页
    TYPE_HOME_PAGE_DAILY_SHOW = 84  # 首页每天展示的
    TYPE_HOME_PAGE_URL = 85  # 首页h5
    TYPE_HOME_PAGE_RECOMMEND = 86  # 首页推荐位
    TYPE_HOME_PAGE_HOT = 87  # 热门内容
    TYPE_ATTENTION_STATUS_NO = 91  # 未关注
    TYPE_ATTENTION_STATUS_YES = 92  # 已关注
    TYPE_ATTENTION_STATUS_EACH_OTHER = 93  # 互相关注
    TYPE_ATTENTION_STATUS_LIST = 94  # 关注列表
    TYPE_ATTENTION_STATUS_BY_LIST = 95  # 被关注列表
    TYPE_OPEN_CLIENT = 221  # 打开应用
    TYPE_OPEN_URL = 222  # 打开连接
    TYPE_OPEN_DETAIL = 223  # 打开详情

    ES_ENUM = {
        TYPE_USER: {"id": "res_id", "doc_type": ES_TYPE_USER,
                    "weight": ES_WEIGHT_USER},
        TYPE_VIDEO_PLAY: {"id": "res_id", "doc_type": ES_TYPE_VIDEO,
                          "weight": ES_WEIGHT_VIDEO},
        TYPE_ARTICLE: {"id": "res_id", "doc_type": ES_TYPE_ARTICLE,
                       "weight": ES_WEIGHT_ARTICLE},
        TYPE_AUDIO: {"id": "res_id", "doc_type": ES_TYPE_AUDIO,
                     "weight": ES_WEIGHT_AUDIO},
        TYPE_COLLECTION: {"id": "res_id", "doc_type": ES_TYPE_COLLECTION,
                          "weight": ES_WEIGHT_COLLECTION}
    }

    TYPE_DEL = 1
    TYPE_UNDEL = 0

    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 12
    DEFAULT_NO_PAGINATE_PER_PAGE = 10000
    DEFAULT_AGE = 18
    DEFAULT_GENDER = 0
    DEFAULT_IS_DEL = 0
    DEFAULT_PORTRAIT = 'http://pic.hopapapa.com/static/Mask@2x.png'
    DEFAULT_USER_STATUS = TYPE_USER_ANONYMOUS  # 匿名用户

    ARTICLE_HTML_URL_FORMAT = 'http://www.hopapapa.com/fabu/news.html?id={}'

    MAX_START = 4638873600

    HEAD_AUTHORIZATION = 'authorization'

    TIMESTAMP_FORMAT_SQL = "%Y-%m-%dT%H:%M:%S"

    ALIYUN_APP_KEY = 'LTAIju7LLMDLbHFx'
    ALIYUN_APP_SECRET = 't4KwSvtg3Wzg9r1HuCpRZkzplGOshD'
    ALIYUN_BUCKET_FILE = 'file-hopapapa-com'
    ALIYUN_BUCKET_IMG = 'img-hopapapa-com'
    ALIYUN_BUCKET_PIC = 'pic-hopapapa-com'

    ALIYUN_IMAGE_SUFFIX_X400PX = '?x-oss-process=image/resize,m_lfit,w_400,limit_0/auto-orient,0/quality,q_90'
    ALIYUN_IMAGE_SUFFIX_X100PX = '?x-oss-process=image/resize,m_lfit,w_100,limit_0/auto-orient,0/quality,q_90'

    CODE_TEMPLATE_ID1 = '3061150'  # 您的验证码为：%s，10分钟有效，打死都不要告诉别人哦。

    # 输出日志文件
    METRICS_LOG_FILE = './metrics.flask.log'
    # 地址前缀
    APPLICATION_ROOT = '/api/v1'
    APPLICATION_ROOT_ADMIN = '/admin/v1'

    LETV_USER_UNIQUE = 'n219pmijzi'
    LETV_KEY_SECRET = '903a9e5bb69205153cab2d5648ceb151'
    LETV_VIDEO_API_URL = 'http://api.letvcloud.com/open.php'

    BAIDU_MAP_AK = 'yeFdiSFZ0fm9CS7iTfEcbHkcBLVhSgRE'

    UMENG_KEY = '58fc8647c62dca72ec001abe'
    UMENG_SECRET = '8gvb4jjymhe9gvpsrppk8a1rpaiz4qps'
    #UMENG_KEY = '58fc7ea94544cb4e4200099d'
    #UMENG_SECRET = 'pnbiq4kukmhadesq052tdi7zjfeeu1xw'

    WANGYI_APP_KEY = '7111da94518f669569422abc553bcd6e'
    WANGYI_APP_SECRET = 'ce35762de9ce'


    # 401   没有权限
    # 403   无法执行操作
