#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: views_urls.py.py
@time: 18-11-1 上午5:06
"""
from __future__ import absolute_import

from django.urls import path

from ..views.masterconfig import MasterConfigCreateView, MasterConfigListView,MasterConfigUpdateView

app_name = 'sqlaudits'


urlpatterns = [
    path('masterconfig/', MasterConfigListView.as_view(), name='masterconfig-list'),
    path('masterconfig/create/', MasterConfigCreateView.as_view(), name='masterconfig-create'),
    path('masterconfig/<int:pk>/update/', MasterConfigUpdateView.as_view(), name='masterconfig-update'),
]