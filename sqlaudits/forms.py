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
from .models import MasterConfig, MasterUser
from django.utils.translation import gettext_lazy as _

class MasterConfigCreateUpdateForm(forms.ModelForm):

    master_password = forms.CharField(
        label=_('Master Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )

    class Meta:
        model = MasterConfig
        fields = [
            'name', 'master_host', 'master_port', 'master_user','master_password'
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


    # def save(self, commit=True):
    #     # master_password = self.cleaned_data.get('master_password')
    #     # master_port = self.cleaned_data.get('master_port')
    #     # master_password = generate_random_password(32)
    #     masterconfig = super().save(commit=commit)
    #     # if master_password:
    #     #     masterconfig.set_password(master_password)
    #     #     masterconfig.save()
    #
    #     return masterconfig




class MasterUserCreateUpdateForm(forms.ModelForm):

    password = forms.CharField(
        label=_('Master Password'), widget=forms.PasswordInput,
        max_length=128, strip=False
    )


    class Meta:
        model = MasterUser
        fields = [
            'master_config_id', 'name', 'clients_host'
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
