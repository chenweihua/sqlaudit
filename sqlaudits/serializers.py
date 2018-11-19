#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: serializers.py
@time: 18-10-28 下午10:00
"""


from rest_framework import serializers
from .models import MasterConfig, MasterUser, MasterPrivilege,MasterUerPrivilege,\
    MasterUserSend,Workflow,SlaveConfig, MasterNetwork, MasterSchema



class LzMasterConfigSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterConfig
        fields = '__all__'


class LzMasterSchemaSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterSchema
        fields = '__all__'


class LzMasterNetworkSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterNetwork
        fields = '__all__'



class LzMasterUserSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterUser
        fields = '__all__'



class LzMasterPrivilegeSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterPrivilege
        fields = '__all__'


class LzMasterUerPrivilegeSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterUerPrivilege
        fields = '__all__'

class LzMasterUserSendSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MasterUserSend
        fields = '__all__'
class LzSlaveConfigSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = SlaveConfig
        fields = '__all__'

class LzWorkflowSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = Workflow
        fields = '__all__'