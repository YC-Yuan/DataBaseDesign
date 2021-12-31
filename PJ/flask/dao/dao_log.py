from constants.info import *
from dao import dao_core
import pymysql as sql
import utils

'''
    日志相关操作
'''


#   获取全部日志
def get_log_info():
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        select_sql = "SELECT * FROM log;"
        cursor.execute(select_sql)
        rows = utils.dict_fetch_all(cursor)
        return rows
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   添加日志
def insert_log(username, operation):
    update_sql = 'INSERT INTO log (username, operation, date) VALUES ("%s", "%s", "%s")' \
                 % (username, operation, utils.get_current_date())
    return update_sql


#   修改日志
def modify_log(log_id, username, operation, date):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        date = utils.string_to_date(date)
        update_sql = "UPDATE log SET username = %s, operation = %s, date = %s WHERE log_id = %s"
        cursor.execute(update_sql, (username, operation, date, log_id,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   删除日志
def delete_log(log_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        delete_sql = "DELETE FROM log WHERE log_id = %s"
        cursor.execute(delete_sql, (log_id,))
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
