from dao import dao_core
from constants import info
import pymysql as sql

'''
    User功能：
    获取用户ID
    获取用户用户名
    删除用户
    查询用户身份
'''


#   获取用户ID
def get_user_id(username):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT user_id FROM employee WHERE username = %s"
    cursor.execute(select_sql, (username,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(username))
    return row[0]


#   获取用户名
def get_user_name(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT name FROM employee WHERE user_id = %s"
    cursor.execute(select_sql, (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(user_id))
    return row[0]


#   查询用户
def has_user(username, password):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "select count(*) from user where username= %s and password= %s"
    cursor.execute(select_sql, (username, password))
    count = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return count > 0


#   删除用户
def delete_employee(username):
    delete_sql = 'DELETE FROM user WHERE username = "%s"' % username
    dao_core.execute_sql(delete_sql)


#   查询用户身份
def get_role_by_username(username):
    if is_admin(username):
        return info.ADMIN
    user_id = get_user_id(username)
    if is_staff(user_id):
        return info.STAFF
    if is_instructor(user_id):
        return info.INSTRUCTOR
    if is_leader(user_id):
        return info.LEADER


def is_admin(username):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "select count(*) from admin where username= %s"
    cursor.execute(select_sql, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_staff(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "select count(*) from staff where user_id= %s"
    cursor.execute(select_sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_instructor(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "select count(*) from instructor where user_id= %s"
    cursor.execute(select_sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_leader(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "select count(*) from leader where user_id= %s"
    cursor.execute(select_sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0
