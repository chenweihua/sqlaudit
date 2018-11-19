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
from .models import MasterConfig, MasterUser, MasterNetwork, MasterPrivilege, MasterSchema, \
    MasterUerPrivilege
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
            'name', 'network_value', 'network_expression'
        ]
        help_texts = {
            'name': '* required',
            'network_value': '* required',
            'network_expression': '* required',

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterNetworkCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterPrivilegeCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = MasterPrivilege
        fields = [
            'name', 'privilege'
        ]
        help_texts = {
            'name': '* required',
            'privilege': '* required',

        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterPrivilegeCreateUpdateForm, self).__init__(*args, **kwargs)


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
        widgets = {
            'charset': forms.RadioSelect(attrs={
                'class': 'select2', 'data-placeholder': _('Nodes')
            }),
            'admin_user': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Admin user')
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Label')
            }),
            'port': forms.TextInput(),
            'domain': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Domain')
            }),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterSchemaCreateUpdateForm, self).__init__(*args, **kwargs)


class MasterUserCreateForm(forms.ModelForm):
    class Meta:
        model = MasterUser
        fields = [
            'masterconfig', 'name', 'network'
        ]
        help_texts = {
            'masterconfig': '* required',
            'name': '* required',
            'network': '* required',
        }

        widgets = {
            'masterconfig': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Masterconfig')
            }),

            'network': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Network')
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterUserCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        password = generate_random_password(32)
        masteruser = super().save(commit=commit)
        if password:
            masteruser.set_password(password)
            masteruser.save()
        return masteruser


class MasterUserUpdateForm(forms.ModelForm):
    class Meta:
        model = MasterUser
        fields = [
            'masterconfig', 'name', 'network'
        ]
        help_texts = {
            'masterconfig': '* required',
            'name': '* required',
            'network': '* required',
        }

        widgets = {
            'masterconfig': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Masterconfig')
            }),

            'network': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Network')
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterUserCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        masteruser = super().save(commit=commit)
        return masteruser


class MasterUserPrivilegesForm(forms.ModelForm):
    class Meta:
        model = MasterUerPrivilege
        fields = [
            'masterprivilege', 'masteruser', 'masterschema', 'tables', 'is_grants',
        ]
        help_texts = {
            'masterconfig': '* required',
            'masteruser': '* required',
            'masterschema': '* required',
        }

        widgets = {
            'masterprivilege': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('MasterPrivilege')
            }),

            'masteruser': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('MasterUser')
            }),

            'masterschema': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('MasterSchema')
            }),
            'tables': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Tables')
            }),
            'tables': forms.RadioSelect(attrs={
                'class': 'select2', 'data-placeholder': _('Tables')
            })
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(MasterUserPrivilegesForm, self).__init__(*args, **kwargs)
