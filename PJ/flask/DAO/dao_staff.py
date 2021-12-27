import datetime

from constants.info import *
import pymysql as sql
from dao.dao_core import *
import utils


#   获取用户信息
def get_user_info(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM employee WHERE user_id = %s"
        cursor.execute(select_sql, (user_id,))
        info = utils.dict_fetch_one(cursor)
        info['hire_date'] = utils.date_to_string(info['hire_date'])
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return info


#   获取用户课程信息
def get_take_courses(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        #   未完成
        courses = []
        #   已完成
        history = []
        select_sql = "SELECT * FROM take WHERE user_id = %s"
        cursor.execute(select_sql, (user_id,))
        #   获取所有的课程id
        rows = cursor.fetchall()
        for row in rows:
            select_sql = "SELECT * FROM course WHERE course_id = %s"
            cursor.execute(select_sql, (row[1],))
            course = utils.dict_fetch_one(cursor)
            course['start_time'] = utils.date_to_string(course['start_time'])
            course['end_time'] = utils.date_to_string(course['end_time'])
            course['instructor'] = get_user_name(course['user_id'])
            course.pop('user_id')
            #   已通过的课程
            if row[2] is not None and row[2] == PASSED:
                course['evaluation'] = PASSED
                select_sql = "SELECT * FROM participate WHERE user_id = %s AND course_id = %s"
                cursor.execute(select_sql, (user_id, row[1],))
                tests = utils.dict_fetch_all(cursor)
                for test in tests:
                    test.pop('user_id')
                    test.pop('course_id')
                course['tests'] = tests
                history.append(course)
            #   未完成的课程
            else:
                courses.append(course)
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return courses, history
