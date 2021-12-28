from constants.info import *
from dao import dao_user, dao_core
import pymysql as sql
import utils

'''
    职员功能：
    获取全部员工信息
    获取某部门下全部员工信息
    根据姓名查询
    根据员工号查询
    修改用户信息
'''


#   获取全部员工信息
def get_employee_info():
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM employee;"
        cursor.execute(select_sql)
        user_infos = utils.dict_fetch_all(cursor)
        for user in user_infos:
            user['hire_date'] = utils.date_to_string(user['hire_date'])
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   按姓名查询员工信息
def search_employee_by_name(name):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM employee WHERE name = %s"
        cursor.execute(select_sql, (name,))
        e_info = cursor.fetchall()
        take_info = []
        for employee in e_info:
            user_id = employee[0]
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
def search_employee_by_uid(user_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
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
    cmd_list = []
    insert_sql = 'INSERT INTO user VALUES("%s", "%s");' % (username, pwd)
    hire_date = utils.string_to_date(hire_date)
    cmd_list.append(insert_sql)
    insert_sql = 'INSERT INTO employee VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' \
                  % (user_id, username, name, gender, age, hire_date, city, telephone, email, dept_name)
    cmd_list.append(insert_sql)
    if role == STAFF:
        insert_sql = 'INSERT INTO staff VALUES("%s");' % user_id
    elif role == INSTRUCTOR:
        insert_sql = 'INSERT INTO instructor VALUES ("%s", "%s");' % (user_id, office_date)
    elif role == LEADER:
        insert_sql = 'INSERT INTO leader VALUES ("%s", "%s", "%s");' % (user_id, office_date, dept_name)
    else:
        return False
    cmd_list.append(insert_sql)
    dao_core.execute_sql_list(cmd_list)
    return True


# 用户修改信息
def modify_info(user_id, city, telephone, email):
    cmd = 'UPDATE employee SET city= "%s",telephone= "%s",email= "%s" ' \
          'WHERE user_id= "%s"' % (city, telephone, email, user_id)
    dao_core.execute_sql(cmd)