#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: masterconfig.py
@time: 18-11-1 上午4:53
"""


from __future__ import unicode_literals


from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView
from django.db import transaction
from django.views.generic.edit import (
    CreateView, UpdateView, FormView
)
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.conf import  settings
from ..models import MasterUser, MasterConfig
from .. import  forms
from users.utils import AdminUserRequiredMixin, get_object_or_none
from common.mixins import JSONResponseMixin
from common.utils import get_logger
from common.const import create_success_msg, update_success_msg



__all__ = [
    'MasterUserListView', 'MasterUserCreateView', 'MasterUserUpdateView',

]

logger = get_logger(__name__)


class MasterUserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'sqlaudit/masterconfig_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': 'Master Config',
            'action': 'MasterUser list',
        })
        return context


class MasterUserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = MasterUser
    form_class = forms.MasterUserCreateUpdateForm
    template_name = 'sqlaudit/masterconfig_create.html'
    success_url = reverse_lazy('sqlaudits:masterconfig-list')
    success_message = create_success_msg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'app': _('Master Config'),
                        'action': _('Create masterconfig'),
                        'masterconfigs': MasterConfig.objects.all(),
                        })
        return context

    def form_valid(self, form):
        masterconfig = form.save(commit=False)
        masterconfig.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MasterUserCreateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs


class MasterUserUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MasterUser
    form_class = forms.MasterUserCreateUpdateForm
    template_name = 'sqlaudit/masterconfig_update.html'
    context_object_name = 'masterconfig_object'
    success_url = reverse_lazy('sqlaudits:masterconfig-list')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        context = {
            'app': _('MasterUser'),
            'action': _('Update MasterUser'),
            'master_user': MasterConfig.objects.all(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        if not password:
            return super().form_valid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MasterUserUpdateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs
