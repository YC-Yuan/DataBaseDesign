from constants.info import *
import pymysql as sql
from dao.dao import *
import utils

ADMIN = "ADMIN"

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


'''
    用户相关操作
'''


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


'''
   添加员工，该处默认数据没问题
   需要检查的数据如下
   user_id 11位数字
   gender 男或女
   hire_date 和 office_date 字符串格式为 %Y/%M/%D
   telephone 和 email 格式正确
'''


def add_Employee(username, pwd, user_id, name, gender, age, hire_date, city, telephone, email, dept_name,
                 role=STAFF, office_date=None):
    try:
        conn = get_db()
        cursor = conn.cursor()
        dept_id = get_dept_id(cursor, dept_name)
        hire_date = utils.StringToDate(hire_date)
        insert_sql = "INSERT INTO user VALUES(%s, %s);"
        cursor.execute(insert_sql, (username, pwd,))
        insert_sql = "INSERT INTO employee VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_sql, (user_id, username, name, gender, age, hire_date, city, telephone, email,))
        insert_sql = "INSERT INTO belong VALUES(%s, %s);"
        cursor.execute(insert_sql, (user_id, dept_id,))
        if role == STAFF:
            add_staff(cursor, user_id)
            print("Admin add_staff " + user_id)
        elif role == INSTRUCTOR:
            add_instructor(cursor, user_id, office_date)
            print("Admin add_instructor " + user_id)
        elif role == LEADER:
            add_leader(cursor, user_id, office_date, dept_id)
            print("Admin add_leader " + user_id)
        else:
            raise sql.MySQLError("Invalid Role")
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()


def add_staff(cursor, user_id):
    insert_sql = "INSERT INTO staff VALUES(%s);"
    cursor.execute(insert_sql, (user_id,))


def add_instructor(cursor, user_id, office_date):
    office_date = utils.StringToDate(office_date)
    insert_sql = "INSERT INTO instructor VALUE (%s, %s);"
    cursor.execute(insert_sql, (user_id, office_date,))


def add_leader(cursor, user_id, office_date, dept_id):
    office_date = utils.StringToDate(office_date)
    insert_sql = "INSERT INTO leader VALUE (%s, %s);"
    cursor.execute(insert_sql, (user_id, office_date,))
    insert_sql = "INSERT INTO charge VALUES (%s, %s);"
    cursor.execute(insert_sql, (user_id, dept_id))


'''
    日志相关操作
'''


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
