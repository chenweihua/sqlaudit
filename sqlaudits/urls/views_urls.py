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

from .. import views


app_name = 'sqlaudits'


urlpatterns = [
    path('masterconfig/', views.MasterConfigListView.as_view(), name='masterconfig-list'),
    path('masterconfig/create/', views.MasterConfigCreateView.as_view(), name='masterconfig-create'),
    path('masterconfig/<int:pk>/update/', views.MasterConfigUpdateView.as_view(), name='masterconfig-update'),
    path('masteruser/', views.MasterUserListView.as_view(), name='masteruser-list'),
    path('masteruser/create/', views.MasterUserCreateView.as_view(), name='masteruser-create'),
    path('masteruser/<int:pk>/update/', views.MasterUserUpdateView.as_view(), name='masteruser-update'),
    path('masternetwork/', views.MasterNetworkListView.as_view(), name='masternetwork-list'),
    path('masternetwork/create/', views.MasterNetworkCreateView.as_view(), name='masternetwork-create'),
    path('masternetwork/<int:pk>/update/', views.MasterNetworkUpdateView.as_view(), name='masternetwork-update'),
    path('masterprivilege/', views.MasterPrivilegeListView.as_view(), name='masterprivilege-list'),
    path('masterprivilege/create/', views.MasterPrivilegeCreateView.as_view(), name='masterprivilege-create'),
    path('masterprivilege/<int:pk>/update/', views.MasterPrivilegeUpdateView.as_view(), name='masterprivilege-update'),
    path('masterschema/', views.MasterSchemaListView.as_view(), name='masterschema-list'),
    path('masterschema/create/', views.MasterSchemaCreateView.as_view(), name='masterschema-create'),
    path('masterschema/<int:pk>/update/', views.MasterSchemaUpdateView.as_view(), name='masterschema-update'),
]