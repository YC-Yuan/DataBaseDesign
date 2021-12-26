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



def is_staff(username):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from staff where username= %s"
    cursor.execute(sql, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_instructor(username):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from instructor where username= %s"
    cursor.execute(sql, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def is_leader(username):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from leader where username= %s"
    cursor.execute(sql, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0


def get_role_by_username(username):
    if is_admin(username):
        return info.ADMIN
    if is_staff(username):
        return info.STAFF
    if is_instructor(username):
        return info.INSTRUCTOR
    if is_leader(username):
        return info.LEADER
