#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''启动程序'''
__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

import os

from flask_restless import APIManager
from flask import render_template
from flask import make_response
from flask import send_file

from src import app
from src import db
from src.admin import restless_service
from src.api import restless_service



