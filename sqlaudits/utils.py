#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""
@version: ??
@author: chenwh
@license: Apache Licence 
@contact: endoffight@gmail.com
@site: 
@software: PyCharm
@file: utils.py
@time: 18-11-3 上午1:52
"""

import random
import string
from collections import namedtuple
from django.conf import  settings
from .con_database import SQLgo

'''
$#!^等特殊字符，在shell下的mysql命令行里面不识别
#特殊字符，在java下不识别
$特殊字符，在php下不识别
'''
SPECIAL_CHARS = '~%&*-_'
PASSWORD_CHARS = string.ascii_letters + string.digits + SPECIAL_CHARS


def generate_random_password(password_length=32):
    """
    生成指定长度的密码字符串，当密码长度超过3时，密码中至少包含：
    1个大写字母+1个小写字母+1个特殊字符
    :param password_length:密码字符串的长度
    :return:密码字符串
    """
    char_list = list()
    char_list.extend(random.sample(string.ascii_uppercase,1))
    char_list.extend(random.sample(string.digits,1))
    char_list.extend(random.sample(string.ascii_lowercase,1))
    char_list.extend(random.sample(SPECIAL_CHARS,1))
    char_list = random.sample(PASSWORD_CHARS,4)
    # char_list = [
    #     random.choice(string.ascii_lowercase),
    #     random.choice(string.ascii_uppercase),
    #     random.choice(SPECIAL_CHARS),
    # ]
    if password_length > 8:
        # random.choice 方法返回一个列表，元组或字符串的随机项
        # (x for x in range(N))返回一个Generator对象
        # [x for x in range(N)] 返回List对象
        char_list.extend([random.choice(PASSWORD_CHARS) for _ in range(password_length - 8)])
    # 使用random.shuffle来将list中元素打乱
    random.shuffle(char_list)
    return ''.join(char_list[0:password_length])


def test_password_generate():
    random_password = generate_random_password(password_length=32)
    print(random_password)


def conf_path() -> object:
    '''
    读取配置文件属性
    '''
    conf_set = namedtuple("name", ["db", "address", "port", "username", "password", "ipaddress"])

    return conf_set(settings.CONFIG.DB_NAME, settings.CONFIG.DB_HOST,
                    settings.CONFIG.DB_PORT ,settings.CONFIG.DB_USER,
                    settings.CONFIG.DB_PASSWORD, settings.CONFIG.DB_HOST)

def init_conf():
    with SQLgo(
            ip = settings.CONFIG.DB_HOST,
            user=settings.CONFIG.DB_USER,
            password=settings.CONFIG.DB_PASSWORD,
            db=settings.CONFIG.DB_NAME,
            port=settings.CONFIG.DB_PORT) as f:
        res = f.query_info("select * from core_globalpermissions where authorization = 'global'")

    return res[0]



