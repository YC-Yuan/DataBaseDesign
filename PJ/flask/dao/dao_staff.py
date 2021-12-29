from constants.info import *
from dao import dao_user, dao_core, dao_dept, dao_log, dao_participate
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


'''
    根据课程结果的状态和类型查找
    :param  dept_name   部门名称
    :param  course      课程编号/类型
    :param  evaluation  成绩状态(None, UNSELECTED, PASSED, FAILED)
    :param  is_category 是否为课程类型
    :return 员工号 员工姓名 课程ID 课程名 课程类型 成绩状态
'''


def search_by_course_and_evaluation(dept_name, course, is_category, evaluation=None):
    try:
        conn = dao_core.get_db()
        cursor = conn.cursor()
        #   按课程类型搜索
        if is_category is True:
            #   选了类型课的人
            if evaluation is None:
                search_sql = 'SELECT * FROM (SELECT * FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff) AS A ' \
                             'NATURAL JOIN (SELECT * FROM ' \
                             '(SELECT course_id, name as c_name, category FROM course WHERE category = "%s") AS C ' \
                             'NATURAL JOIN take) AS B' % (dept_name, course)
            #   一个类型课都没选的人
            elif evaluation == UNSELECTED:
                search_sql = 'SELECT user_id, name, NULL as course_id, NULL as c_name, "%s" as category, "%s" as evaluation FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff ' \
                             'WHERE user_id NOT IN (SELECT user_id FROM (SELECT course_id FROM course WHERE category = "%s") AS C ' \
                             'NATURAL JOIN take)' % (course, UNSELECTED, dept_name, course);
            #   选了类型课且规定成绩状态
            else:
                search_sql = 'SELECT * FROM (SELECT * FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff) AS A ' \
                             'NATURAL JOIN (SELECT * FROM ' \
                             '(SELECT course_id, name as c_name, category FROM course WHERE category = "%s") AS C ' \
                             'NATURAL JOIN take WHERE evaluation = "%s") AS B' % (dept_name, course, evaluation)
        else:
            #   选了该课的人
            if evaluation is None:
                search_sql = 'SELECT * FROM (SELECT * FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff) AS A ' \
                             'NATURAL JOIN (SELECT * FROM ' \
                             '(SELECT course_id, name as c_name, category FROM course WHERE course_id = "%s") AS C ' \
                             'NATURAL JOIN take) AS B' % (dept_name, course)
            #   没选的人
            elif evaluation == UNSELECTED:
                search_sql = 'SELECT user_id, name, "%s" as course_id, NULL as c_name, NULL as category, "%s" as evaluation FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff ' \
                             'WHERE user_id NOT IN (SELECT user_id FROM (SELECT course_id FROM course WHERE course_id = "%s") AS C ' \
                             'NATURAL JOIN take)' % (course, UNSELECTED, dept_name, course);
            #   选了课且规定成绩状态
            else:
                search_sql = 'SELECT * FROM (SELECT * FROM ' \
                             '(SELECT user_id, name FROM employee WHERE dept_name = "%s") AS E NATURAL JOIN staff) AS A ' \
                             'NATURAL JOIN (SELECT * FROM ' \
                             '(SELECT course_id, name as c_name, category FROM course WHERE course_id = "%s") AS C ' \
                             'NATURAL JOIN take WHERE evaluation = "%s") AS B' % (dept_name, course, evaluation)
        cursor.execute(search_sql)
        infos = utils.dict_fetch_all(cursor)
        for info in infos:
            info['tests'] = []
            if evaluation != UNSELECTED:
                info['tests'] = dao_participate.get_tests_by_uc(info['user_id'], info['course_id'])
        print(infos)
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
