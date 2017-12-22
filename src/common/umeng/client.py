#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''umeng工具类'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.common.umeng.base import UmengBase


class UmengPush(UmengBase):
    def push_ios_all(self, alert, custom_params=None):
        return self.call_push(
            type='broadcast',
            alert=alert,
            custom_params=custom_params
        )

    def push_ios(self, alert, device_token, custom_params=None):
        return self.call_push(
            type='unicast',
            alert=alert,
            device_token=device_token,
            custom_params=custom_params
        )


if __name__ == '__main__':
    up = UmengPush(key='58fc7ea94544cb4e4200099d',
                   secret='pnbiq4kukmhadesq052tdi7zjfeeu1xw')
    # up = UmengPush()
    # res = up.push_ios_all('睡毛，起来嗨')
    res = up.push_ios(
        alert='跳转网址',
        device_token='cb985a8075241905f0c2e3d5e849f53015b565ab333a0353c39cefa574212006',
        custom_params={
            'open_type': 222,
            'url': 'http://baidu.com'
        })
    # res = up.push_ios_all(
    #     alert='跳转网址',
    #     custom_params={
    #         'open_type': 222,
    #         'url': 'http://baidu.com'
    #     })
    print(res)
