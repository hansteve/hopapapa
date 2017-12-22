#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''base64工具'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import base64

data = "1111;,/11"

encoded = base64.b64encode(data)
print ("编码后（%d字节）：%r" % (len(encoded), encoded))

decoded = base64.b64decode(encoded)
print ("复原后（%d字节）：%r" % (len(decoded), decoded))


