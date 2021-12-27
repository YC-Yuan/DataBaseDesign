from constants.info import *
import pymysql as sql
from DAO.dao import *
import utils


''' 教师相关功能 '''


#   创建课程
def create_course(instructor_id, course_id, name, content, category, start_time, end_time):
    try:
        conn = get_db()
        cursor = conn.cursor()
        start_time = utils.string_to_date(start_time)
        end_time = utils.string_to_date(end_time)
        insert_sql = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, (course_id, name, content, category, start_time, end_time, instructor_id,))
        conn.commit()
        print(instructor_id + " add_course " + course_id)
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   设置课程要求
#   require: obligatory(必修) elective(选修) disable(不可选)
def set_course_require(course_id, dept_name, require):
    try:
        conn = get_db()
        cursor = conn.cursor()
        dept_id = get_dept_id(dept_name)
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
        print("set_course " + course_id + " " + require + " " + dept_name)
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   获取教师教的课的信息
def get_courses(instructor_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM course WHERE instructor_id = %s"
        cursor.execute(select_sql, (instructor_id,))
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


#   获取某一门课的学生的信息(私有方法)
def __get_course_student(course_id):
    try:
        conn = get_db()
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


#   录入成绩
def score_input(user_id, course_id, score):
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT end_time FROM course WHERE course_id = %s"
        cursor.execute(select_sql, (course_id,))
        row = cursor.fetchone()
        if utils.check_course_end(row[0]):
            select_sql = "SELECT evaluation FROM take WHERE user_id = %s AND course_id = %s"
            cursor.execute(select_sql, (user_id, course_id,))
            eva = cursor.fetchone()[0]
            if eva == PASSED:
                raise sql.MySQLError("禁止卷逼刷分")
            insert_sql = "INSERT INTO participate VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_sql, (user_id, course_id, utils.get_current_timestamp(), score,))
            #   及格则自动修改状态
            if score >= PASS_LINE:
                update_sql = "UPDATE take SET evaluation = %s WHERE user_id = %s AND course_id = %s"
                cursor.execute(update_sql, (PASSED, user_id, course_id,))
            conn.commit()
            print("score_input " + str(user_id) + " " + str(course_id) + " " + str(score))
        else:
            raise sql.MySQLError("尚未结课")
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
