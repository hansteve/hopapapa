#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''aliyun工具类'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import oss2

from src.config import BaseConfig

auth = oss2.Auth(BaseConfig.ALIYUN_APP_KEY, BaseConfig.ALIYUN_APP_SECRET)

ENDPOINT = 'http://oss-cn-beijing.aliyuncs.com'


def put_object(key, data, bucket_name, headers=None):
    '''上传文本'''
    bucket = oss2.Bucket(auth, ENDPOINT, bucket_name)

    res = bucket.put_object(
        key=key,
        data=data,
        headers=headers
    )


    if res.status == 200:
        return make_url_header(bucket_name) + key
    else:
        return None


def make_url_header(bucket):
    url = bucket.replace('-', '.')
    return 'http://{}/'.format(url)


if __name__ == '__main__':
    s = 'file-hopapapa-com'.replace('-', '.')
    print(s)
    url = put_object('test/test.txt', '你好', 'file-hopapapa-com')
    print(url)


