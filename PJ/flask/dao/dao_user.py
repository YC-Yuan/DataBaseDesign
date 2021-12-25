from dao import dao
from constants import info


def has_user(username, password):
    conn = dao.get_db()
    cursor = conn.cursor()
    sql = "select count(*) from user where username= %s and password= %s"
    cursor.execute(sql, (username, password))
    count = cursor.fetchall()[0][0]
    return count > 0


def is_admin(username):
    # TODO
    pass


def is_staff(username):
    # TODO
    pass


def is_instructor(username):
    # TODO
    pass


def is_leader(username):
    # TODO
    pass


def get_role_by_username(username):
    if is_admin(username):
        return info.ADMIN
    if is_staff(username):
        return info.STAFF
    if is_instructor(username):
        return info.INSTRUCTOR
    if is_leader(username):
        return info.LEADER
