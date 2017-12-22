#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''article表service'''

__author__ = "wenxiaoning(371032668@qq.com)"
__copyright__ = "Copyright of hopapapa (2017)."

from src.api.article.models import Article


def get_articles(**params):
    arts = Article.query_articles(**params)
    print(arts)

    items = []
    for item in arts:
        items.append(item.to_json())

    return items
