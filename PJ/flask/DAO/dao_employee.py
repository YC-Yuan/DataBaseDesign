from constants.info import *
from dao import dao_user, dao_core
import pymysql as sql
import utils


# 用户修改信息
def modify_info(user_id, city, telephone, email):
    cmd = 'update employee set city= "%s",telephone= "%s",email= "%s" ' \
          'where user_id= "%s"' % (city, telephone, email, user_id)
    dao_core.execute_sql(cmd)
