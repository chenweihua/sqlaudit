from django.db import models

from .aes_decryptor import Prpcrypt
from .utils import generate_random_password

# Create your models here.


# 各个线上主库地址。
class MasterConfig(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('集群名称', max_length=50, unique=True)
    master_host = models.CharField('主库地址', max_length=200)
    master_port = models.IntegerField('主库端口', default=3306)
    master_user = models.CharField('登录主库的用户名', max_length=100)
    master_password = models.CharField('登录主库的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_master_config'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.master_password = pc.encrypt(self.master_password)
        super(MasterConfig, self).save(*args, **kwargs)


# 各个线上主库地址。
class MasterSchema(models.Model):
    id = models.AutoField(primary_key=True)
    masterconfig= models.ForeignKey('MasterConfig', on_delete=models.CASCADE)
    name = models.CharField('集群名称', max_length=50, unique=True)
    charset = models.CharField(max_length=12, choices=(('utf8','utf8'),("utf8mb4", 'utf8mb4')))
    charset_type = models.CharField(max_length=32, blank=False, null=False)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_master_schema'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.master_password = pc.encrypt(self.master_password)
        super(MasterConfig, self).save(*args, **kwargs)


class MasterUser(models.Model):
    id = models.AutoField(primary_key=True)
    masterconfig= models.ForeignKey('MasterConfig', on_delete=models.CASCADE)
    name = models.CharField('登录主库的用户名', max_length=18)
    # password = models.CharField('登录主库的密码', max_length=64)
    network = models.ManyToManyField('MasterNetwork')
    privileges = models.ManyToManyField('MasterPrivilege',through ='MasterUerPrivilege')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name+'@'+self.client_host

    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    #: Use this attr to set user object password, example
    #: user = User(username='example', password_raw='password', ...)
    #: It's equal:
    #: user = User(username='example', ...)
    #: user.set_password('password')
    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    def set_password(self, raw_password):
        self._set_password = True
        return super().set_password(raw_password)



    class Meta:
        db_table = 'lz_master_user'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'

    def save(self, *args, **kwargs):
        # password = generate_random_password(32)
        pc = Prpcrypt()  # 初始化
        self.password = pc.encrypt(self.password)
        super(MasterUser, self).save(*args, **kwargs)


class MasterPrivilege(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('登录权',max_length=32)
    privilege = models.CharField('登录权', max_length=255)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_master_privilage'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'


class MasterNetwork(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('',max_length=32)
    network_value = models.CharField('登录权', max_length=255)
    network_expression = models.CharField(max_length=32,null=False ,blank=False,default='localhost')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_master_network'
        verbose_name = u'配置'
        verbose_name_plural = u'配置'


class MasterUerPrivilege(models.Model):
    id = models.AutoField(primary_key=True)
    masterprivilege = models.ForeignKey(MasterPrivilege, blank=True, null=True,
                                  verbose_name='主库地址配置id', on_delete=models.CASCADE)
    masteruser= models.ForeignKey(MasterUser, blank=True, null=True,
                                  verbose_name='主库地址配置id', on_delete=models.CASCADE)
    masterschema = models.ForeignKey(MasterSchema, blank=True, null=True,
                                  verbose_name='主库地址配置id', on_delete=models.CASCADE)
    tables = models.TextField("主库")
    is_grants = models.IntegerField('授权', default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.schemas

    class Meta:
        db_table = 'lz_master_user_privilage'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'



class MasterUserSend(models.Model):
    id = models.AutoField(primary_key=True)
    masteruser= models.ForeignKey(MasterUser, blank=True, null=True,
                                  verbose_name='主库地址配置id', on_delete=models.CASCADE)
    email = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_master_user_send'
        verbose_name = u'主库地址配置'
        verbose_name_plural = u'主库地址配置'

# 各个线上从库地址
class SlaveConfig(models.Model):
    id = models.AutoField(primary_key=True)
    cluster_name = models.CharField('集群名称', max_length=50, unique=True)
    slave_host = models.CharField('从库地址', max_length=200)
    slave_port = models.IntegerField('从库端口', default=3306)
    slave_user = models.CharField('登录从库的用户名', max_length=100)
    slave_password = models.CharField('登录从库的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


    class Meta:
        db_table = 'lz_slave_config'
        verbose_name = u'从库地址配置'
        verbose_name_plural = u'从库地址配置'

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.slave_password = pc.encrypt(self.slave_password)
        super(SlaveConfig, self).save(*args, **kwargs)



# 存放各个SQL上线工单的详细内容，可定期归档或清理历史数据，也可通过alter table workflow row_format=compressed; 来进行压缩
class Workflow(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('工单内容', max_length=50)
    engineer = models.CharField('发起人', max_length=50)
    review_man = models.CharField('审核人', max_length=50)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    finish_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.CharField(max_length=50, choices=(
        ('已正常结束', '已正常结束'), ('人工终止流程', '人工终止流程'), ('自动审核中', '自动审核中'), ('等待审核人审核', '等待审核人审核'), ('审核通过', '审核通过'),
        ('定时执行', '定时执行'), ('执行中', '执行中'), ('自动审核不通过', '自动审核不通过'), ('执行有异常', '执行有异常')))
    # is_backup = models.IntegerField('是否备份，0为否，1为是', choices=((0,0),(1,1)))
    is_backup = models.CharField('是否备份', choices=(('否', '否'), ('是', '是')), max_length=20)
    review_content = models.TextField('自动审核内容的JSON格式')
    cluster_name = models.CharField('集群名称', max_length=50)
    reviewok_time = models.DateTimeField('人工审核通过的时间', null=True, blank=True)
    sql_content = models.TextField('具体sql内容')
    execute_result = models.TextField('执行结果的JSON格式', blank=True)
    is_manual = models.IntegerField('是否手工执行', choices=((0, '否'), (1, '是')), default=0)
    audit_remark = models.TextField('审核备注', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lz_workflow'
        verbose_name = u'SQL工单管理'
        verbose_name_plural = u'SQL工单管理'





# 工作流审核主表
class WorkflowAudit(models.Model):
    id = models.AutoField(primary_key=True)
    # Workflow_id = models.BigIntegerField('关联业务id')
    workflow = models.ForeignKey(Workflow, blank=True, null=True,
                                  verbose_name='主库地址配置id', on_delete=models.CASCADE)
    workflow_type = models.IntegerField('申请类型',
                                        choices=((1, '查询权限申请'),))
    name = models.CharField('申请标题', max_length=50,default='', null=False,blank=False)
    workflow_remark = models.CharField('申请备注', default='', max_length=140)
    audit_users = models.CharField('审核人列表', max_length=255)
    current_audit_user = models.CharField('当前审核人', max_length=20)
    next_audit_user = models.CharField('下级审核人', max_length=20)
    current_status = models.IntegerField('审核状态', choices=((0, '待审核'), (1, '审核通过'), (2, '审核不通过'), (3, '审核取消')))
    create_user = models.CharField('申请人', max_length=20)
    create_time = models.DateTimeField('申请时间', auto_now_add=True)
    sys_time = models.DateTimeField('系统时间', auto_now=True)

    def __int__(self):
        return self.name

    class Meta:
        db_table = 'lz_workflow_audit'
        unique_together = ('workflow', 'workflow_type')
        verbose_name = u'工作流列表'
        verbose_name_plural = u'工作流列表'


# 审批明细表
class WorkflowAuditDetail(models.Model):
    id = models.AutoField(primary_key=True)
    workauditflow = models.ForeignKey(WorkflowAudit,  verbose_name='审核主表id', blank=True, null=True,
    on_delete=models.CASCADE)
    audit_user = models.CharField('审核人', max_length=20)
    audit_time = models.DateTimeField('审核时间')
    audit_status = models.IntegerField('审核状态', choices=((0, '待审核'), (1, '审核通过'), (2, '审核不通过'), (3, '审核取消')), )
    remark = models.CharField('审核备注', default='', max_length=140)
    sys_time = models.DateTimeField('系统时间', auto_now=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'lz_workflow_audit_detail'
        verbose_name = u'审批明细表'
        verbose_name_plural = u'审批明细表'


# 审批配置表
class WorkflowAuditSetting(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, null=False,default='')
    workflow_type = models.IntegerField('申请类型,', choices=((1, '查询权限申请'),), unique=True)
    audit_users = models.CharField('审核人，单人审核格式为：user1，多级审核格式为：user1,user2', max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.name

    class Meta:
        db_table = 'lz_workflow_audit_setting'
        verbose_name = u'工作流配置'
        verbose_name_plural = u'工作流配置'


# 查询权限申请记录表
class QueryPrivilegesApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    title = models.CharField('申请标题', max_length=50)
    user_name = models.CharField('申请人', max_length=30)
    cluster_name = models.CharField('集群名称', max_length=50)
    db_list = models.TextField('数据库')
    table_list = models.TextField('表')
    valid_date = models.DateField('有效时间')
    limit_num = models.IntegerField('行数限制', default=100)
    priv_type = models.IntegerField('权限类型', choices=((1, 'DATABASE'), (2, 'TABLE'),), default=0)
    status = models.IntegerField('审核状态', choices=((0, '待审核'), (1, '审核通过'), (2, '审核不通过'), (3, '审核取消')), )
    create_time = models.DateTimeField(auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.apply_id

    class Meta:
        db_table = 'lz_query_privileges_apply'
        verbose_name = u'查询权限申请记录表'
        verbose_name_plural = u'查询权限申请记录表'


# 用户权限关系表
class QueryPrivileges(models.Model):
    privilege_id = models.AutoField(primary_key=True)
    user_name = models.CharField('用户名', max_length=30)
    cluster_name = models.CharField('集群名称', max_length=50)
    db_name = models.CharField('数据库', max_length=200)
    table_name = models.CharField('表', max_length=200)
    valid_date = models.DateField('有效时间')
    limit_num = models.IntegerField('行数限制', default=100)
    priv_type = models.IntegerField('权限类型', choices=((1, 'DATABASE'), (2, 'TABLE'),), default=0)
    is_deleted = models.IntegerField('是否删除', default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.privilege_id

    class Meta:
        db_table = 'lz_query_privileges'
        verbose_name = u'查询权限记录表'
        verbose_name_plural = u'查询权限记录表'


# 记录在线查询sql的日志
class QueryLog(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)
    db_name = models.CharField('数据库名称', max_length=30)
    sqllog = models.TextField('执行的sql查询')
    effect_row = models.BigIntegerField('返回行数')
    cost_time = models.CharField('执行耗时', max_length=10, default='')
    username = models.CharField('操作人', max_length=30)
    create_time = models.DateTimeField('操作时间', auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lz_query_log'
        verbose_name = u'sql查询日志'
        verbose_name_plural = u'sql查询日志'


# 脱敏字段配置
class DataMaskingColumns(models.Model):
    column_id = models.AutoField('字段id', primary_key=True)
    rule_type = models.IntegerField('规则类型',
                                    choices=((1, '手机号'), (2, '证件号码'), (3, '银行卡'), (4, '邮箱'), (5, '金额'), (6, '其他')))
    active = models.IntegerField('激活状态', choices=((0, '未激活'), (1, '激活')))
    cluster_name = models.CharField('集群名称', max_length=50)
    table_schema = models.CharField('字段所在库名', max_length=64)
    table_name = models.CharField('字段所在表名', max_length=64)
    column_name = models.CharField('字段名', max_length=64)
    column_comment = models.CharField('字段描述', max_length=1024, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    sys_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lz_data_masking_columns'
        verbose_name = u'脱敏字段配置'
        verbose_name_plural = u'脱敏字段配置'


# 脱敏规则配置
class DataMaskingRules(models.Model):
    rule_type = models.IntegerField('规则类型',
                                    choices=((1, '手机号'), (2, '证件号码'), (3, '银行卡'), (4, '邮箱'), (5, '金额'), (6, '其他')), unique=True)
    rule_regex = models.CharField('规则脱敏所用的正则表达式，表达式必须分组，隐藏的组会使用****代替', max_length=255)
    hide_group = models.IntegerField('需要隐藏的组')
    rule_desc = models.CharField('规则描述', max_length=100, default='', blank=True)
    sys_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lz_data_masking_rules'
        verbose_name = u'脱敏规则配置'
        verbose_name_plural = u'脱敏规则配置'


# 记录阿里云的认证信息
class AliyunAccessKey(models.Model):
    ak = models.CharField(max_length=50)
    secret = models.CharField(max_length=100)
    is_enable = models.IntegerField(choices=((1, '启用'), (2, '禁用')))
    remark = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        db_table = 'lz_aliyun_access_key'
        verbose_name = u'阿里云认证信息'
        verbose_name_plural = u'阿里云认证信息'

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.ak = pc.encrypt(self.ak)
        self.secret = pc.encrypt(self.secret)
        super(AliyunAccessKey, self).save(*args, **kwargs)


# 阿里云rds配置信息
class AliyunRdsConfig(models.Model):
    name = models.OneToOneField(MasterConfig, db_constraint=False, to_field='name',blank=True, null=True,
                                        db_column='name', verbose_name='集群名称', unique=True, on_delete=models.SET_NULL)
    rds_dbinstanceid = models.CharField('阿里云RDS实例ID', max_length=100)

    def __int__(self):
        return self.rds_dbinstanceid

    class Meta:
        db_table = 'lz_aliyun_rds_config'
        verbose_name = u'阿里云rds配置'
        verbose_name_plural = u'阿里云rds配置'


# SlowQuery
class SlowQuery(models.Model):
    checksum = models.CharField(max_length=32, primary_key=True)
    fingerprint = models.TextField()
    sample = models.TextField()
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True, db_index=True)
    reviewed_by = models.CharField(max_length=20, blank=True, null=True)
    reviewed_on = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lz_mysql_slow_query_review'
        verbose_name = u'慢日志统计'
        verbose_name_plural = u'慢日志统计'


# SlowQueryHistory
class SlowQueryHistory(models.Model):
    hostname_max = models.CharField(max_length=64, null=False)
    client_max = models.CharField(max_length=64, null=True)
    user_max = models.CharField(max_length=64, null=False)
    db_max = models.CharField(max_length=64, null=True, default=None)
    bytes_max = models.CharField(max_length=64, null=True)
    checksum = models.ForeignKey(SlowQuery, db_constraint=False, blank=True, null=True, to_field='checksum', db_column='checksum',on_delete=models.SET_NULL)
    sample = models.TextField()
    ts_min = models.DateTimeField(db_index=True)
    ts_max = models.DateTimeField()
    ts_cnt = models.FloatField(blank=True, null=True)
    query_time_sum = models.FloatField(db_column='Query_time_sum', blank=True, null=True)
    query_time_min = models.FloatField(db_column='Query_time_min', blank=True, null=True)
    query_time_max = models.FloatField(db_column='Query_time_max', blank=True, null=True)
    query_time_pct_95 = models.FloatField(db_column='Query_time_pct_95', blank=True, null=True)
    query_time_stddev = models.FloatField(db_column='Query_time_stddev', blank=True, null=True)
    query_time_median = models.FloatField(db_column='Query_time_median', blank=True, null=True)
    lock_time_sum = models.FloatField(db_column='Lock_time_sum', blank=True, null=True)
    lock_time_min = models.FloatField(db_column='Lock_time_min', blank=True, null=True)
    lock_time_max = models.FloatField(db_column='Lock_time_max', blank=True, null=True)
    lock_time_pct_95 = models.FloatField(db_column='Lock_time_pct_95', blank=True, null=True)
    lock_time_stddev = models.FloatField(db_column='Lock_time_stddev', blank=True, null=True)
    lock_time_median = models.FloatField(db_column='Lock_time_median', blank=True, null=True)
    rows_sent_sum = models.FloatField(db_column='Rows_sent_sum', blank=True, null=True)
    rows_sent_min = models.FloatField(db_column='Rows_sent_min', blank=True, null=True)
    rows_sent_max = models.FloatField(db_column='Rows_sent_max', blank=True, null=True)
    rows_sent_pct_95 = models.FloatField(db_column='Rows_sent_pct_95', blank=True, null=True)
    rows_sent_stddev = models.FloatField(db_column='Rows_sent_stddev', blank=True, null=True)
    rows_sent_median = models.FloatField(db_column='Rows_sent_median', blank=True, null=True)
    rows_examined_sum = models.FloatField(db_column='Rows_examined_sum', blank=True, null=True)
    rows_examined_min = models.FloatField(db_column='Rows_examined_min', blank=True, null=True)
    rows_examined_max = models.FloatField(db_column='Rows_examined_max', blank=True, null=True)
    rows_examined_pct_95 = models.FloatField(db_column='Rows_examined_pct_95', blank=True, null=True)
    rows_examined_stddev = models.FloatField(db_column='Rows_examined_stddev', blank=True, null=True)
    rows_examined_median = models.FloatField(db_column='Rows_examined_median', blank=True, null=True)
    rows_affected_sum = models.FloatField(db_column='Rows_affected_sum', blank=True, null=True)
    rows_affected_min = models.FloatField(db_column='Rows_affected_min', blank=True, null=True)
    rows_affected_max = models.FloatField(db_column='Rows_affected_max', blank=True, null=True)
    rows_affected_pct_95 = models.FloatField(db_column='Rows_affected_pct_95', blank=True, null=True)
    rows_affected_stddev = models.FloatField(db_column='Rows_affected_stddev', blank=True, null=True)
    rows_affected_median = models.FloatField(db_column='Rows_affected_median', blank=True, null=True)
    rows_read_sum = models.FloatField(db_column='Rows_read_sum', blank=True, null=True)
    rows_read_min = models.FloatField(db_column='Rows_read_min', blank=True, null=True)
    rows_read_max = models.FloatField(db_column='Rows_read_max', blank=True, null=True)
    rows_read_pct_95 = models.FloatField(db_column='Rows_read_pct_95', blank=True, null=True)
    rows_read_stddev = models.FloatField(db_column='Rows_read_stddev', blank=True, null=True)
    rows_read_median = models.FloatField(db_column='Rows_read_median', blank=True, null=True)
    merge_passes_sum = models.FloatField(db_column='Merge_passes_sum', blank=True, null=True)
    merge_passes_min = models.FloatField(db_column='Merge_passes_min', blank=True, null=True)
    merge_passes_max = models.FloatField(db_column='Merge_passes_max', blank=True, null=True)
    merge_passes_pct_95 = models.FloatField(db_column='Merge_passes_pct_95', blank=True, null=True)
    merge_passes_stddev = models.FloatField(db_column='Merge_passes_stddev', blank=True, null=True)
    merge_passes_median = models.FloatField(db_column='Merge_passes_median', blank=True, null=True)
    innodb_io_r_ops_min = models.FloatField(db_column='InnoDB_IO_r_ops_min', blank=True, null=True)
    innodb_io_r_ops_max = models.FloatField(db_column='InnoDB_IO_r_ops_max', blank=True, null=True)
    innodb_io_r_ops_pct_95 = models.FloatField(db_column='InnoDB_IO_r_ops_pct_95', blank=True, null=True)
    innodb_io_r_ops_stddev = models.FloatField(db_column='InnoDB_IO_r_ops_stddev', blank=True, null=True)
    innodb_io_r_ops_median = models.FloatField(db_column='InnoDB_IO_r_ops_median', blank=True, null=True)
    innodb_io_r_bytes_min = models.FloatField(db_column='InnoDB_IO_r_bytes_min', blank=True, null=True)
    innodb_io_r_bytes_max = models.FloatField(db_column='InnoDB_IO_r_bytes_max', blank=True, null=True)
    innodb_io_r_bytes_pct_95 = models.FloatField(db_column='InnoDB_IO_r_bytes_pct_95', blank=True, null=True)
    innodb_io_r_bytes_stddev = models.FloatField(db_column='InnoDB_IO_r_bytes_stddev', blank=True, null=True)
    innodb_io_r_bytes_median = models.FloatField(db_column='InnoDB_IO_r_bytes_median', blank=True, null=True)
    innodb_io_r_wait_min = models.FloatField(db_column='InnoDB_IO_r_wait_min', blank=True, null=True)
    innodb_io_r_wait_max = models.FloatField(db_column='InnoDB_IO_r_wait_max', blank=True, null=True)
    innodb_io_r_wait_pct_95 = models.FloatField(db_column='InnoDB_IO_r_wait_pct_95', blank=True, null=True)
    innodb_io_r_wait_stddev = models.FloatField(db_column='InnoDB_IO_r_wait_stddev', blank=True, null=True)
    innodb_io_r_wait_median = models.FloatField(db_column='InnoDB_IO_r_wait_median', blank=True, null=True)
    innodb_rec_lock_wait_min = models.FloatField(db_column='InnoDB_rec_lock_wait_min', blank=True, null=True)
    innodb_rec_lock_wait_max = models.FloatField(db_column='InnoDB_rec_lock_wait_max', blank=True, null=True)
    innodb_rec_lock_wait_pct_95 = models.FloatField(db_column='InnoDB_rec_lock_wait_pct_95', blank=True, null=True)
    innodb_rec_lock_wait_stddev = models.FloatField(db_column='InnoDB_rec_lock_wait_stddev', blank=True, null=True)
    innodb_rec_lock_wait_median = models.FloatField(db_column='InnoDB_rec_lock_wait_median', blank=True, null=True)
    innodb_queue_wait_min = models.FloatField(db_column='InnoDB_queue_wait_min', blank=True, null=True)
    innodb_queue_wait_max = models.FloatField(db_column='InnoDB_queue_wait_max', blank=True, null=True)
    innodb_queue_wait_pct_95 = models.FloatField(db_column='InnoDB_queue_wait_pct_95', blank=True, null=True)
    innodb_queue_wait_stddev = models.FloatField(db_column='InnoDB_queue_wait_stddev', blank=True, null=True)
    innodb_queue_wait_median = models.FloatField(db_column='InnoDB_queue_wait_median', blank=True, null=True)
    innodb_pages_distinct_min = models.FloatField(db_column='InnoDB_pages_distinct_min', blank=True, null=True)
    innodb_pages_distinct_max = models.FloatField(db_column='InnoDB_pages_distinct_max', blank=True, null=True)
    innodb_pages_distinct_pct_95 = models.FloatField(db_column='InnoDB_pages_distinct_pct_95', blank=True, null=True)
    innodb_pages_distinct_stddev = models.FloatField(db_column='InnoDB_pages_distinct_stddev', blank=True, null=True)
    innodb_pages_distinct_median = models.FloatField(db_column='InnoDB_pages_distinct_median', blank=True, null=True)
    qc_hit_cnt = models.FloatField(db_column='QC_Hit_cnt', blank=True, null=True)
    qc_hit_sum = models.FloatField(db_column='QC_Hit_sum', blank=True, null=True)
    full_scan_cnt = models.FloatField(db_column='Full_scan_cnt', blank=True, null=True)
    full_scan_sum = models.FloatField(db_column='Full_scan_sum', blank=True, null=True)
    full_join_cnt = models.FloatField(db_column='Full_join_cnt', blank=True, null=True)
    full_join_sum = models.FloatField(db_column='Full_join_sum', blank=True, null=True)
    tmp_table_cnt = models.FloatField(db_column='Tmp_table_cnt', blank=True, null=True)
    tmp_table_sum = models.FloatField(db_column='Tmp_table_sum', blank=True, null=True)
    tmp_table_on_disk_cnt = models.FloatField(db_column='Tmp_table_on_disk_cnt', blank=True, null=True)
    tmp_table_on_disk_sum = models.FloatField(db_column='Tmp_table_on_disk_sum', blank=True, null=True)
    filesort_cnt = models.FloatField(db_column='Filesort_cnt', blank=True, null=True)
    filesort_sum = models.FloatField(db_column='Filesort_sum', blank=True, null=True)
    filesort_on_disk_cnt = models.FloatField(db_column='Filesort_on_disk_cnt', blank=True, null=True)
    filesort_on_disk_sum = models.FloatField(db_column='Filesort_on_disk_sum', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lz_mysql_slow_query_review_history'
        unique_together = ('checksum', 'ts_min', 'ts_max')
        index_together = ('hostname_max', 'ts_min')
        verbose_name = u'慢日志明细'
        verbose_name_plural = u'慢日志明细'