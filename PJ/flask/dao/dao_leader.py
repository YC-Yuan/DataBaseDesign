from constants.info import *
import pymysql as sql
from dao import dao_core, dao_dept, dao_log
import utils


def get_dept_by_leader(user_id):
    cmd = 'select dept_name from leader ' \
          'where user_id= %s'
    conn = dao_core.get_db()
    cursor = conn.cursor()
    cursor.execute(cmd, user_id)
    dept = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return dept


#   按员工号给员工安排课程
def arrange_staff_course(username, user_id, course_id, dept_name):
    cmd_list = []
    insert_sql = 'INSERT INTO take (user_id, course_id) SELECT "%s", "%s" FROM dual WHERE NOT EXISTS' \
                 '(SELECT * FROM take WHERE user_id = "%s" AND course_id = "%s")' % (user_id, course_id, user_id, course_id)
    operation = 'arrange course %s for %s' % (course_id, user_id)
    log_sql = dao_log.insert_log(username, operation)
    cmd_list.append(insert_sql)
    cmd_list.append(log_sql)
    dao_core.execute_sql_list(cmd_list)


#   检测员工属于部门且为普通员工
def __check_employee_in_dept(cursor, user_id, dept_name):
    select_sql = "SELECT COUNT(*) FROM employee WHERE user_id = %s AND dept_name = %s AND EXISTS " \
                 "(SELECT * FROM staff WHERE user_id = %s)"
    cursor.execute(select_sql, (user_id, dept_name, user_id))
    if cursor.fetchone()[0] == 0:
        raise sql.MySQLError("没有权限")


#   检测课程属于部门
def __check_course_in_dept(cursor, course_id, dept_id):
    select_sql = "SELECT need FROM offer WHERE course_id = %s AND dept_id = %s"
    cursor.execute(select_sql, (course_id, dept_id,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("没有权限")
    elif row[0] == MANDATORY:
        raise sql.MySQLError("没有必要")
