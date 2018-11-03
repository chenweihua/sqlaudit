#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: masterconfig.py.py
@time: 18-11-2 上午6:09
"""


from rest_framework.viewsets import ModelViewSet
from rest_framework_bulk import BulkModelViewSet
from ..serializers import LzMasterConfigSerializer, LzMasterUserSerializer
from ..models import MasterConfig, MasterUser,MasterPrivilege, MasterNetwork

class LzMasterConfigViewSet(BulkModelViewSet):
    """
    System user api set, for add,delete,update,list,retrieve resource
    """
    queryset = MasterConfig.objects.all()
    serializer_class = LzMasterConfigSerializer
    filter_fields = ('name', 'master_host', 'master_user')


class LzMasterUserViewSet(BulkModelViewSet):
    """
    System user api set, for add,delete,update,list,retrieve resource
    """
    queryset = MasterUser.objects.all()
    serializer_class = LzMasterUserSerializer
    filter_fields = ('username', 'master_host', 'master_user')
