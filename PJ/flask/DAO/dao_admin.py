from constants.info import *
import pymysql as sql
from DAO.dao import *
import utils

# 每个事务都要创建连接


''' 管理员相关功能 '''


def get_employee_info():
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM employee;"
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        print(rows)
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_course_info():
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM course;"
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        print(rows)
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_log_info():
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM log;"
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        print(rows)
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


'''
    用户相关操作
'''


#   按姓名查询员工信息
def search_staff_by_name(name):
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM staff WHERE name = %s"
        cursor.execute(select_sql, (name,))
        staff_info = cursor.fetchall()
        take_info = []
        for staff in staff_info:
            user_id = staff[0]
            select_sql = "SELECT * FROM take WHERE user_id = %s"
            cursor.execute(select_sql, (user_id,))
            take_info.append(cursor.fetchone())
        # TODO

    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   按员工号查询员工信息
def search_staff_by_name(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        select_sql = "SELECT * FROM staff WHERE user_id = %s"
        cursor.execute(select_sql, (user_id,))
        staff_info = cursor.fetchone()
        select_sql = "SELECT * FROM take WHERE user_id = %s"
        cursor.execute(select_sql, (user_id,))
        take_info = cursor.fetchall()
        # TODO

    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   删除用户
def delete_Employee(username):
    try:
        conn = get_db()
        cursor = conn.cursor()
        delete_sql = "DELETE FROM user WHERE username = %s"
        cursor.execute(delete_sql, (username,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


'''
   添加员工，该处默认数据没问题
   需要检查的数据如下
   user_id 11位数字
   gender 男或女
   hire_date 和 office_date 字符串格式为 %Y/%M/%D
   telephone 和 email 格式正确
'''


def insert_employee(username, pwd, user_id, name, gender, age, hire_date, city, telephone, email, dept_name,
                    role=STAFF, office_date=None):
    try:
        conn = get_db()
        cursor = conn.cursor()
        hire_date = utils.string_to_date(hire_date)
        insert_sql = "INSERT INTO user VALUES(%s, %s);"
        cursor.execute(insert_sql, (username, pwd,))
        insert_sql = "INSERT INTO employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, (user_id, username, name, gender, age, hire_date, city, telephone, email, dept_name))
        if role == STAFF:
            insert_staff(cursor, user_id)
            print("Admin add_staff " + user_id)
        elif role == INSTRUCTOR:
            insert_instructor(cursor, user_id, office_date)
            print("Admin add_instructor " + user_id)
        elif role == LEADER:
            insert_leader(cursor, user_id, office_date, dept_name)
            print("Admin add_leader " + user_id)
        else:
            raise sql.MySQLError("Invalid Role")
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_staff(cursor, user_id):
    insert_sql = "INSERT INTO staff VALUES(%s);"
    cursor.execute(insert_sql, (user_id,))


def insert_instructor(cursor, user_id, office_date):
    office_date = utils.string_to_date(office_date)
    insert_sql = "INSERT INTO instructor VALUES (%s, %s);"
    cursor.execute(insert_sql, (user_id, office_date,))


def insert_leader(cursor, user_id, office_date, dept_name):
    office_date = utils.string_to_date(office_date)
    insert_sql = "INSERT INTO leader VALUES (%s, %s, %s);"
    cursor.execute(insert_sql, (user_id, office_date, dept_name,))


'''
    课程相关操作
'''


#   添加课程
def insert_course(instructor_id, course_id, name, content, category, start_time, end_time):
    try:
        conn = get_db()
        cursor = conn.cursor()
        start_time = utils.string_to_date(start_time)
        end_time = utils.string_to_date(end_time)
        insert_sql = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, (course_id, name, content, category, start_time, end_time, instructor_id,))
        conn.commit()
        print("Admin add_course " + course_id)
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
        print("Admin set_course " + course_id + " " + require + " " + dept_name)
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   删除课程
def delete_course(course_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        delete_sql = "DELETE FROM course WHERE course_id = %s"
        cursor.execute(delete_sql, (course_id,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


'''
    日志相关操作
'''


#   添加日志
def insert_log(operation, date):
    try:
        conn = get_db()
        cursor = conn.cursor()
        update_sql = "INSERT INTO log (operation, date) VALUES (%s, %s)"
        cursor.execute(update_sql, (operation, utils.string_to_timestamp(date),))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   修改日志
def modify_log(log_id, operation):
    try:
        conn = get_db()
        cursor = conn.cursor()
        update_sql = "UPDATE log SET operation = %s WHERE log_id = %s"
        cursor.execute(update_sql, (operation, log_id,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   删除日志
def delete_log(log_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        delete_sql = "DELETE FROM log WHERE log_id = %s"
        cursor.execute(delete_sql, (log_id,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
