import pymysql as sql
from PJ.flask.dbase.utils import *


def logger(cursor, username, operation):
    date = get_current_timestamp()
    insert_sql = "INSERT INTO log(operation, date) VALUES(%s, %s)"
    cursor.execute(insert_sql, (operation, date,))
    log_id = cursor.lastrowid
    print(log_id)
    insert_sql = "INSERT INTO trace VALUES(%s, %s)"
    cursor.execute(insert_sql, (username, log_id,))
