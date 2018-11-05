#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: masterschema.py
@time: 18-11-1 上午4:53
"""


from __future__ import unicode_literals


from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy, reverse

from django.utils.translation import ugettext as _

from django.views.generic.base import TemplateView

from django.views.generic.edit import (
    CreateView, UpdateView, FormView
)

from ..models import MasterSchema
from .. import  forms
from users.utils import AdminUserRequiredMixin, get_object_or_none
from common.mixins import JSONResponseMixin
from common.utils import get_logger
from common.const import create_success_msg, update_success_msg



__all__ = [
    'MasterSchemaListView', 'MasterSchemaCreateView', 'MasterSchemaUpdateView',

]

logger = get_logger(__name__)


class MasterSchemaListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'sqlaudit/masterschema_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'app': 'Master Schema',
            'action': 'MasterSchema list',
        })
        return context


class MasterSchemaCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = MasterSchema
    form_class = forms.MasterSchemaCreateUpdateForm
    template_name = 'sqlaudit/masterschema_create_update.html'
    success_url = reverse_lazy('sqlaudits:masterschema-list')
    success_message = create_success_msg
    print(success_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'app': _('Master Schema'), 'action': _('Create masterschema')})
        return context


class MasterSchemaUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MasterSchema
    form_class = forms.MasterSchemaCreateUpdateForm
    template_name = 'sqlaudit/masterschema_create_update.html'
    context_object_name = 'masterschema_object'
    success_url = reverse_lazy('sqlaudits:masterschema-list')
    success_message = update_success_msg

    def get_context_data(self, **kwargs):
        # check_rules, min_length = get_password_check_rules()
        context = {
            'app': _('MasterSchema'),
            'action': _('Update MasterSchema'),
            # 'password_check_rules': check_rules,
            # 'min_length': min_length
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

