from constants.info import *
from dao import dao_user, dao_core, dao_dept, dao_log
import pymysql as sql
import utils


#   获取用户信息
def get_user_info(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM employee WHERE user_id = %s"
        cursor.execute(select_sql, (user_id,))
        info = utils.dict_fetch_one(cursor)
        info['hire_date'] = utils.date_to_string(info['hire_date'])
        return info
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   获取某一门课的学生的信息
def get_staff_by_course_id(course_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT * FROM employee AS e WHERE e.user_id IN (SELECT user_id FROM take WHERE course_id = %s)"
    cursor.execute(select_sql, (course_id,))
    students = utils.dict_fetch_all(cursor)
    for student in students:
        student['hire_date'] = utils.date_to_string(student['hire_date'])
    cursor.close()
    conn.close()
    return students


#   转部门
def transfer_dept(username, user_id, dept_name):
    cmd_list = []
    insert_sql = 'UPDATE employee SET dept_name = "%s" WHERE user_id = "%s"' % (dept_name, user_id)
    cmd_list.append(insert_sql)
    dept_id = dao_dept.get_dept_id(dept_name)
    rows = dao_dept.get_dept_mandatory_course(dept_id)
    for row in rows:
        course_id = row[0]
        insert_sql = 'INSERT INTO take (user_id, course_id) SELECT "%s", "%s" FROM dual WHERE NOT EXISTS ' \
                     '(SELECT * FROM take WHERE user_id = "%s" AND course_id = "%s")' % (
                         user_id, course_id, user_id, course_id)
        cmd_list.append(insert_sql)
    operation = 'transfer %s to %s' % (user_id, dept_name)
    log_sql = dao_log.insert_log(username, operation)
    cmd_list.append(log_sql)
    dao_core.execute_sql_list(cmd_list)
