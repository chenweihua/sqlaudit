#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: masternetwork.py
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
from ..models import MasterNetwork
from .. import  forms
from users.utils import AdminUserRequiredMixin, get_object_or_none
from common.mixins import JSONResponseMixin
from common.utils import get_logger
from common.const import create_success_msg, update_success_msg



__all__ = [
    'MasterNetworkListView', 'MasterNetworkCreateView', 'MasterNetworkUpdateView',

]

logger = get_logger(__name__)


class MasterNetworkListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'sqlaudit/masternetwork_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': 'Master Netwrok',
            'action': 'MasterNetwork list',
        })
        return context


class MasterNetworkCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = MasterNetwork
    form_class = forms.MasterNetworkCreateUpdateForm
    template_name = 'sqlaudit/masternetwork_create_update.html'
    success_url = reverse_lazy('sqlaudits:masternetwork-list')
    success_message = create_success_msg
    print(success_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'app': _('Master Config'), 'action': _('Create masternetwork')})
        return context
    #
    # def form_valid(self, form):
    #     masternetwork = form.save(commit=False)
    #     masternetwork.save()
    #     return super().form_valid(form)
    #
    # def get_form_kwargs(self):
    #     kwargs = super(MasterNetworkCreateView, self).get_form_kwargs()
    #     data = {'request': self.request}
    #     kwargs.update(data)
    #     return kwargs


class MasterNetworkUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MasterNetwork
    form_class = forms.MasterNetworkCreateUpdateForm
    template_name = 'sqlaudit/masternetwork_create_update.html'
    context_object_name = 'masternetwork_object'
    success_url = reverse_lazy('sqlaudits:masternetwork-list')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        # check_rules, min_length = get_password_check_rules()
        context = {
            'app': _('MasterNetwork'),
            'action': _('Update MasterNetwork'),
            # 'password_check_rules': check_rules,
            # 'min_length': min_length
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        if not password:
            return super().form_valid(form)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(MasterNetworkUpdateView, self).get_form_kwargs()
        data = {'request': self.request}
        kwargs.update(data)
        return kwargs
