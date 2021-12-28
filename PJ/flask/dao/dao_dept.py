from constants.info import *
from dao import dao_core
import pymysql as sql
import utils

'''
    部门相关操作:
    · 获取部门ID
    · 获取部门下员工
    · 获取部门下课程
    · 获取部门下必修课ID
    · 获取部门下符合转部门情况的员工
'''

'''
    获取部门ID
    :param  dept_name   部门名称
    :return dept_id     部门编号
'''


def get_dept_id(dept_name):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]


'''
    获取部门下必修课ID
    :param  dept_name   部门名称
    :return courses_ids 课程编号
'''


def get_dept_mandatory_course(dept_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT course_id FROM offer WHERE dept_id = %s AND need = %s"
        cursor.execute(select_sql, (dept_id, MANDATORY,))
        rows = cursor.fetchall()
        return rows
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


'''
    获取部门下符合转部门情况的员工
    :param  dept_name   部门名称
    :return user_infos  员工信息
'''


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
    finally:
        cursor.close()
        conn.close()


'''
    获取员工转专业后要学的课程
    :param  user_id     员工号
    :param  dept_name   部门名称
    :return user_infos  员工信息
'''


def get_dept_need_take_course(user_id, dept_name):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        dept_id = get_dept_id(dept_name)
        select_sql = "SELECT * FROM course WHERE course_id IN " \
                     "(SELECT course_id FROM offer WHERE dept_id = %s AND need = %s AND course_id NOT IN" \
                     "(SELECT course_id FROM take WHERE user_id = %s))"
        cursor.execute(select_sql, (dept_id, MANDATORY, user_id,))
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
