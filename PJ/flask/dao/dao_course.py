import dao.dao_core
from constants.info import *
from dao import dao_user, dao_core, dao_dept, dao_participate, dao_log, dao_employee
import pymysql as sql
import utils

'''
    课程相关操作:
    · 获取全部课程
    · 根据员工号搜索历史课程
    · 根据员工号搜索进行课程
    · 获取教师教的课的信息
    · 创建课程
    · 修改课程部分信息（不能改结束时间）
    · 设置课程要求
    · 删除课程
    · 更新课程状态
'''


#   获取全部课程信息
def get_course_info():
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM course;"
        cursor.execute(select_sql)
        courses = utils.dict_fetch_all(cursor)
        for course in courses:
            course['instructor'] = dao_employee.get_employee_name(course['instructor_id'])
            course['start_time'] = utils.date_to_string(course['start_time'])
            course['end_time'] = utils.date_to_string(course['end_time'])
        return courses
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# 根据员工号搜索进行课程
def get_course_by_uid(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        cmd = 'select course_id,name,content,category,start_time,end_time,instructor_id ' \
              'from course natural join (' \
              'select * from take ' \
              'where take.user_id = %s) as t ' \
              'where evaluation != "%s"'
        cursor.execute(cmd, (user_id, PASSED,))
        res = utils.dict_fetch_all(cursor)
        courses = []
        for r in res:
            r['tests'] = dao_participate.get_tests_by_uc(user_id=user_id, course_id=r['course_id'])
            r['start_time'] = utils.date_to_string(r['start_time'])
            r['end_time'] = utils.date_to_string(r['end_time'])
            r['instructor'] = dao_employee.get_employee_name(r['instructor_id'])
            courses.append(r)
        return courses
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# 根据uid搜索员工历史课程
def get_course_history_by_uid(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        cmd = 'select course_id,name,content,category,start_time,end_time,instructor_id ' \
              'from course natural join (' \
              'select * from take ' \
              'where take.user_id = %s) as t ' \
              'where evaluation = "%s"'
        cursor.execute(cmd, (user_id, PASSED,))
        res = cursor.fetchall()
        history = []
        for r in res:
            r['cid'] = r['course_id']
            r['start_time'] = utils.date_to_string(r['start_time'])
            r['end_time'] = utils.date_to_string(r['end_time'])
            r['instructor'] = dao_employee.get_employee_name(r['instructor_id'])
            r.pop('course_id')
            r.pop('instructor_id')
            history.append(r)
        return history
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


'''
    获取部门下课程
    :param  dept_name   部门名称
    :return courses  课程信息
'''


# 根据dept_name搜索课程
def get_course_by_dept_name(dept_name):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT * FROM ((SELECT * FROM offer WHERE dept_id IN (SELECT dept_id FROM department WHERE " \
                 "name = %s)) AS O NATURAL JOIN course)"
    cursor.execute(select_sql, dept_name)
    courses = utils.dict_fetch_all(cursor)
    for course in courses:
        course['start_time'] = utils.date_to_string(course['start_time'])
        course['end_time'] = utils.date_to_string(course['end_time'])
        course['instructor'] = dao_employee.get_employee_name(course['instructor_id'])
    cursor.close()
    conn.close()
    return courses


#   获取教师教的课的信息
def get_courses_by_instructor(instructor_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM course WHERE instructor_id = %s"
        cursor.execute(select_sql, (instructor_id,))
        courses = utils.dict_fetch_all(cursor)
        for course in courses:
            course['start_time'] = utils.date_to_string(course['start_time'])
            course['end_time'] = utils.date_to_string(course['end_time'])
        print(courses)
        return courses
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   创建课程
def insert_course(username, instructor_id, course_id, name, content, category, start_time, end_time):
    cmd_list = []
    operation = "create course %s (instructor: %s)" % (course_id, instructor_id)
    start_time = utils.string_to_date(start_time)
    end_time = utils.string_to_date(end_time)
    insert_sql = 'INSERT INTO course VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % \
                 (course_id, name, content, category, start_time, end_time, instructor_id)
    cmd_list.append(insert_sql)
    log_sql = dao_log.insert_log(username, operation)
    cmd_list.append(log_sql)
    dao_core.execute_sql_list(cmd_list)


def set_course(username, instructor_id, course_id, name, content, category, start_time, end_time):
    cmd = 'update course set ( name="%s",content="%s",category="%s",start_time="%s",end_time="%s",instructor_id="%s"' \
          'where course_id = %s' % (name, content, category, start_time, end_time, instructor_id, course_id)
    dao_core.execute_sql(cmd)
    operation = "modify course %s (instructor: %s)" % (course_id, instructor_id)
    dao_core.execute_sql(dao_log.insert_log(username, operation))


#   设置课程要求
#   require: obligatory(必修) elective(选修) disable(不可选)
def set_course_require(username, course_id, dept_name, require):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        dept_id = dao_dept.get_dept_id(dept_name)
        operation = "set course %s to %s for %s" % (course_id, require,dept_name)
        #   取消课程
        if require == DISABLE:
            delete_sql = "DELETE FROM offer WHERE course_id = %s AND dept_id = %s"
            cursor.execute(delete_sql, (course_id, dept_id,))
        else:
            select_sql = "SELECT COUNT(*) FROM offer WHERE course_id = %s AND dept_id = %s"
            cursor.execute(select_sql, (course_id, dept_id,))
            #   修改要求
            if cursor.fetchone()[0] > 0:
                update_sql = "UPDATE offer SET need = %s WHERE course_id = %s AND dept_id = %s"
                cursor.execute(update_sql, (require, course_id, dept_id,))
            #   增加要求
            else:
                insert_sql = "INSERT INTO offer VALUES (%s, %s, %s);"
                cursor.execute(insert_sql, (dept_id, course_id, require,))
            #   必修课
            if require == MANDATORY:
                select_sql = "SELECT user_id FROM employee AS e WHERE e.dept_name = %s " \
                             "AND EXISTS (SELECT user_id FROM staff AS s WHERE s.user_id = e.user_id)"
                cursor.execute(select_sql, (dept_name,))
                rows = cursor.fetchall()
                for row in rows:
                    user_id = row[0]
                    insert_sql = "INSERT INTO take (user_id, course_id) SELECT %s, %s FROM dual WHERE NOT EXISTS " \
                                 "(SELECT * FROM take WHERE user_id = %s AND course_id = %s)"
                    cursor.execute(insert_sql, (user_id, course_id, user_id, course_id,))
        log_sql = dao_log.insert_log(username, operation)
        cursor.execute(log_sql)
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# 查看是否存在
def has_course(cid):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    cmd = 'select count(*) from course where course_id = %s'
    cursor.execute(cmd, (cid,))
    has = cursor.fetchone()
    return has[0] != 0


#   删除课程
def delete_course(username, course_id):
    cmd_list = []
    delete_sql = 'DELETE FROM course WHERE course_id = "%s"' % course_id
    operation = 'delete course %s' % course_id
    cmd_list.append(delete_sql)
    log_sql = dao_log.insert_log(username, operation)
    cmd_list.append(log_sql)
    dao_core.execute_sql_list(cmd_list)


#   更新课程状态（指结课）
def update_courses_state():
    update_sql = "UPDATE take SET evaluation = '%s' WHERE evaluation IS NULL AND course_id IN " \
                 "(SELECT course_id FROM course WHERE end_time <= now())" % FAILED
    dao_core.execute_sql(update_sql)


def get_course_by_name(name):
    cmd = 'select * from course where name = "%s"' % name
    conn = dao_core.get_db()
    cursor = conn.cursor()
    cursor.execute(cmd)
    course = utils.dict_fetch_one(cursor)
    cursor.close()
    conn.close()
    return course


# 查看课程是否结束
def is_over(course_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT end_time FROM course WHERE course_id = %s;"
        cursor.execute(select_sql, (course_id,))
        row = cursor.fetchone()
        if row is None:
            raise sql.MySQLError("课程不存在")
        return utils.check_course_end(row[0])
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


update_courses_state()
