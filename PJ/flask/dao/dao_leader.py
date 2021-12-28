from constants.info import *
import pymysql as sql
from dao import dao_core, dao_dept
import utils


#   按员工号给员工安排课程
def arrange_staff_course(user_id, course_id, dept_name):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        __check_employee_in_dept(cursor, user_id, dept_name)
        dept_id = dao_dept.get_dept_id(dept_name)
        __check_course_in_dept(cursor, course_id, dept_id)
        insert_sql = "INSERT INTO take (user_id, course_id) SELECT %s, %s FROM dual WHERE NOT EXISTS " \
                     "(SELECT * FROM take WHERE user_id = %s AND course_id = %s)"
        cursor.execute(insert_sql, (user_id, course_id, user_id, course_id,))
        conn.commit()
        print("arrange_staff_course")
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


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
    cursor.execute(select_sql, (course_id, dept_id, ))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("没有权限")
    elif row[0] == MANDATORY:
        raise sql.MySQLError("没有必要")


