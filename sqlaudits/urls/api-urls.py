#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: api-views_urls.py
@time: 18-11-2 上午6:05
"""

from rest_framework_bulk.routes import BulkRouter
from .. import api


app_name = "sqlaudits"

router = BulkRouter()

router.register(r'masterconfig', api.LzMasterConfigViewSet, 'masterconfig')
router.register(r'masteruser', api.LzMasterUserViewSet, 'masteruser')
router.register(r'masternetwork', api.LzMasterUserViewSet, 'masternetwork')
router.register(r'masterprivilege', api.LzMasterUserViewSet, 'masterprivilege')
router.register(r'masterschema', api.LzMasterSchemaViewSet, 'masterschema')
urlpatterns =[

]

urlpatterns += router.urls

