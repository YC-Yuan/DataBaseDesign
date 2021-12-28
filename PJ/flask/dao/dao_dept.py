from constants.info import *
from dao import dao_core
import pymysql as sql
import utils


def get_dept_id(dept_name):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]


#   获取部门下员工
def get_dept_user(dept_name):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM employee WHERE dept_name = %s"
        cursor.execute(select_sql, (dept_name,))
        user_infos = utils.dict_fetch_all(cursor)
        for user in user_infos:
            user['hire_date'] = utils.date_to_string(user['hire_date'])
        print(user_infos)
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   获取部门下课程
def get_dept_course(dept_name):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        dept_id = get_dept_id(dept_name)
        select_sql = "SELECT * FROM ((SELECT * FROM offer WHERE dept_id = %s) AS O NATURAL JOIN course)"
        cursor.execute(select_sql, (dept_id,))
        courses = utils.dict_fetch_all(cursor)
        for course in courses:
            course['start_time'] = utils.date_to_string(course['start_time'])
            course['end_time'] = utils.date_to_string(course['end_time'])
        print(courses)
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   获取部门下必修课ID
def get_dept_mandatory_course(dept_id):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        select_sql = "SELECT course_id FROM offer WHERE dept_id = %s AND need = %s"
        cursor.execute(select_sql, (dept_id, MANDATORY,))
        rows = cursor.fetchall()
        return rows
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   获取部门下符合转部门情况的员工
def get_qualified_staff(dept_name):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM " \
                     "(SELECT * FROM employee NATURAL JOIN staff WHERE dept_name = %s) AS e " \
                     "WHERE NOT EXISTS " \
                     "(SELECT * FROM take WHERE take.user_id = e.user_id AND evaluation != %s)"
        cursor.execute(select_sql, (dept_name, PASSED,))
        user_infos = utils.dict_fetch_all(cursor)
        for user in user_infos:
            user['hire_date'] = utils.date_to_string(user['hire_date'])
        print(user_infos)
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


get_qualified_staff("策划部门")
