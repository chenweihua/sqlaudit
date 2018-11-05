class IncepationRollback(object):
    def __init__(self, LoginDic=None):
        self.__dict__.update(LoginDic)
        self.con = object

    def __enter__(self):
        un_init = util.init_conf()
        inception = ast.literal_eval(un_init['inception'])
        self.con = pymysql.connect(host=inception['host'],
                                   user=inception['user'],
                                   passwd=inception['password'],
                                   port=int(inception['port']),
                                   db='',
                                   charset="utf8")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()
    def __str__(self):
        return '''
        InceptionSQL Class
        '''
    def rollbackSQL(self, db=None, opid=None):
      with con_database.SQLgo(
              ip=inception["back_host"],
              user=inception["back_user"],
              password=inception["back_password"],
              db=db,
              port=inception["back_port"]
      ) as f:
          data = f.query_info(
              sql=
              '''
              select tablename from $_$Inception_backup_information$_$ where opid_time =%s;
              ''' % opid)
          return data[0]
    def roll(backdb=None, opid=None):
      with con_database.SQLgo(
              ip=inception["back_host"],
              user=inception["back_user"],
              password=inception["back_password"],
              port=inception["back_port"]
      ) as f:
          data = f.query_info(
              sql=
              '''
              select rollback_statement from %s where opid_time =%s;
              ''' % (backdb, opid))
          return data
