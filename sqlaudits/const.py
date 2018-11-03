#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: const.py
@time: 18-10-31 上午5:27
"""

PRIVILAGES = {
    'read':'select',
    'app':'select,update,insert',
    'backup': 'select,replicat client ,flush,create trigger, show view',
    'dba': 'select,insert,delete,update,create,alter,drop,replication client',
    'monitor': 'select, REPLICATION CLIENT,process',
    'repl': 'REPLICATION SLAVE,REPLICATION CLIENT',
    'all': 'all',
    'inception': 'select,insert,create'
}