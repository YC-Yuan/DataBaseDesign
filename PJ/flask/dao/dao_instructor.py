from constants.info import *
import pymysql as sql
from dao.dao_core import *
import utils

''' 教师相关功能 '''


#   检查教师权限
def __check_course(cursor, instructor_id, course_id):
    select_sql = "SELECT COUNT(*) FROM course WHERE course_id = %s AND instructor_id = %s"
    cursor.execute(select_sql, (course_id, instructor_id,))
    if cursor.fetchone()[0] == 0:
        raise sql.MySQLError("没有权限")
