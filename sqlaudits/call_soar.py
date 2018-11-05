# -*- coding:utf-8 -*-
import logging
import subprocess
import traceback


from .models import MasterConfig
from .aes_decryptor import Prpcrypt

logger = logging.getLogger('default')


class Soar(object):
    def __init__(self, LoginDic=None):
        self.__dict__.update(LoginDic)
        self.soar_path = '/usr/local/bin/soar'
        self.test_dsn = ''


    # 获取soar的处理结果
    def soar(self, config, dbname, sql):

        result = {'status': 0, 'msg': 'ok', 'data': []}

        # 服务器端参数验证
        if not (config and dbname and sql):
            result['status'] = 1
            result['msg'] = '页面提交参数可能为空'
            return result


        sql = sql.strip().replace('"', '\\"').replace('`', '\`').replace('\n', ' ')
        # 目标实例的连接信息
        instance = MasterConfig.objects.get(name=config)
        online_dsn = "{user}:{pwd}@{host}:{port}/{db}".format(user=instance.master_user,
                                                              pwd=Prpcrypt().decrypt(instance.master_password),
                                                              host=instance.master_host,
                                                              port=instance.master_port,
                                                              db=dbname)
        # 获取测试实例的连接信息和soar程序路径

        if not (self.soar_path and self.test_dsn):
            result['status'] = 1
            result['msg'] = '请配置soar_path和test_dsn！'
            return result

        # 提交给soar获取分析报告
        try:
            p = subprocess.Popen(
                self.soar_path + ' -allow-online-as-test=false -report-type=markdown' +
                ' -query "{}" -online-dsn "{}" -test-dsn "{}" '.format(sql.strip(), online_dsn, self.test_dsn),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True,
                universal_newlines=True)
            stdout, stderr = p.communicate()
            result['data'] = stdout
        except Exception as error:
            logger.error(traceback.format_exc())
            result['status'] = 2
            result['data'] = 'soar运行报错，请检查相关日志'
        return result
