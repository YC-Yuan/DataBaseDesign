import datetime
import pymysql as sql
from PJ.flask.dbase.config import *


# 获取数据库连接
def get_db():
    try:
        db = sql.connect(host=HOST,
                         port=3306,
                         user=USER,
                         password=PWD,
                         database=DB_NAME)
        return db
    except sql.MySQLError as e:
        print(e)
        exit(0)


def StringToDate(string):
    return datetime.datetime.strptime(string, '%Y/%m/%d')


def get_current_timestamp():
    return datetime.datetime.now().timestamp()


def get_dept_id(cursor, dept_name):
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]
