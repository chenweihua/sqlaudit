#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: forms.py
@time: 18-11-1 上午5:31
"""

from django import forms
from .utils import generate_random_password
from .models import MasterConfig, MasterUser, MasterNetwork, MasterPrivilege, MasterSchema
from django.utils.translation import gettext_lazy as _


class MasterConfigCreateUpdateForm(forms.ModelForm):
    master_password = forms.CharField(
        label=_('Master Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )

    class Meta:
        model = MasterConfig
        fields = [
            'name', 'master_host', 'master_port', 'master_user', 'master_password'
        ]
        help_texts = {
            'name': '* required',
            'master_host': '* required',
            'master_user': '* required',
            'master_password': '* required',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterConfigCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterNetworkCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MasterNetwork
        fields = [
            'name', 'network_value'
        ]
        help_texts = {
            'name': '* required',
            'network_value': '* required',

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterConfigCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterSchemaCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MasterSchema
        fields = [
            'name', 'charset', 'charset_type'
        ]
        help_texts = {
            'name': '* required',
            'charset': '* required',

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterSchemaCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterPrivilegeCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MasterPrivilege
        fields = [
            'name', 'privilege'
        ]
        help_texts = {
            'name': '* required',
            'network_value': '* required',

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterConfigCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterUserCreateUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Master Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )

    class Meta:
        model = MasterUser
        fields = [
            'masterconfig', 'name', 'network'
        ]
        help_texts = {
            'master_config_id': '* required',
            'name': '* required',
            'clients_host': '* required',
        }

        widgets = {
            'master_config_id': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('MastConfig')
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterUserCreateUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        password = generate_random_password(32)
        masteruser = super().save(commit=commit)
        if password:
            masteruser.set_password(password)
            masteruser.save()
        return masteruser
