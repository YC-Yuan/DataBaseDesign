from constants.info import *
from dao import dao_user, dao_core, dao_dept
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


#   获取用户课程信息
def get_take_courses(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
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
            course['instructor'] = dao_user.get_user_name(course['user_id'])
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
        return courses, history
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   获取某一门课的学生的信息
def get_course_student(course_id):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM employee AS e WHERE e.user_id IN (SELECT user_id FROM take WHERE course_id = %s)"
        cursor.execute(select_sql, (course_id,))
        students = utils.dict_fetch_all(cursor)
        for student in students:
            student['hire_date'] = utils.date_to_string(student['hire_date'])
        print(students)
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   转部门
def transfer_dept(user_id, dept_name):
    cmd_list = []
    insert_sql = 'UPDATE employee SET dept_name = "%s" WHERE user_id = "%s"' % (dept_name, user_id)
    cmd_list.append(insert_sql)
    dept_id = dao_dept.get_dept_id(dept_name)
    rows = dao_dept.get_dept_mandatory_course(dept_id)
    for row in rows:
        course_id = row[0]
        insert_sql = 'INSERT INTO take (user_id, course_id) SELECT "%s", "%s" FROM dual WHERE NOT EXISTS ' \
                     '(SELECT * FROM take WHERE user_id = "%s" AND course_id = "%s")' % (user_id, course_id, user_id, course_id)
        cmd_list.append(insert_sql)
    dao_core.execute_sql_list(cmd_list)

