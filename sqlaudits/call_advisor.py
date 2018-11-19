# -*- coding: UTF-8 -*-
import logging
import subprocess
import traceback


from django.http import HttpResponse
from .aes_decryptor import Prpcrypt
from django.conf import settings
from .models import  MasterConfig
import os

logger = logging.getLogger('default')


class Sqladvisor(object):
    def __init__(self):
        self.sqladvisor_path = settings.SQLADVISOR_PATH


    def sqladvisor(self, instance_name, sql_content, db_name,verbose):

        result = {'status': 0, 'msg': 'ok', 'data': []}

        # 服务器端参数验证
        if sql_content is None or instance_name is None:
            result['status'] = 1
            result['msg'] = '页面提交参数可能为空'
            return result

        sql_content = sql_content.strip()


        if os.path.isfile(self.sqladvisor_path) is False:

            result['status'] = 1
            result['msg'] = '页面提交参数可能为空'
            return result

        if verbose is None or verbose == '':
            verbose = 1

        # 取出主库的连接信息
        instance_info = MasterConfig.objects.get(name=instance_name)

        # 提交给sqladvisor获取审核结果

        sql_content = sql_content.strip().replace('"', '\\"').replace('`', '\`').replace('\n', ' ')
        try:
            p = subprocess.Popen(self.sqladvisor_path + ' -h "%s" -P "%s" -u "%s" -p "%s\" -d "%s" -v %s -q "%s"' % (
                str(instance_info.host), str(instance_info.port), str(instance_info.user),
                str(Prpcrypt().decrypt(instance_info.password), ), str(db_name), verbose, sql_content),
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            stdout, stderr = p.communicate()
            result['data'] = stdout
        except Exception:
            result["status"] = 2
            logger.error(traceback.format_exc())
            result['data'] = 'sqladvisor运行报错，请检查日志'
        return result
