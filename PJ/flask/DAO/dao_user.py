from dao import dao
from constants import info


def has_user(username, password):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from user where username= %s and password= %s"
    cursor.execute(sql, (username, password))
    count = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return count > 0


def is_admin(username):
    # TODO
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from admin where username= %s"
    cursor.execute(sql, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_staff(user_id):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from employee where user_id= %s"
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_instructor(user_id):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from instructor where user_id= %s"
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_leader(user_id):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from leader where user_id= %s"
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def get_role_by_username(username):
    if is_admin(username):
        return info.ADMIN
    user_id = dao.get_user_id(username)
    if is_staff(user_id):
        return info.STAFF
    if is_instructor(user_id):
        return info.INSTRUCTOR
    if is_leader(user_id):
        return info.LEADER
