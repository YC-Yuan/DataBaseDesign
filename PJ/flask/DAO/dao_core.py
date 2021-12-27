import pymysql as sql
from config import *
import init_data


def init_db():
    sql_drop_db = 'drop database if exists ' + DB_NAME
    sql_create_db = 'CREATE DATABASE if not exists ' + DB_NAME
    db = sql.connect(host=HOST,
                     port=3306,
                     user=USER,
                     password=PWD)
    cursor = db.cursor()
    cursor.execute(sql_drop_db)
    cursor.execute(sql_create_db)
    cursor.close()
    db.close()


def execute_sql_file(f):
    db = get_db()
    cursor = db.cursor()
    try:
        sql_list = f.read().split(';')[:-1]
        for x in sql_list:
            if '\n' in x:
                # 脚本换行处替换为空格
                x = x.replace('\n', ' ')
            x += ';'
            print(x)
            cursor.execute(x)
        db.commit()
    except sql.MySQLError as e:
        print(e)
        db.rollback()
        exit(0)
    finally:
        cursor.close()
        db.close()


def init_tables():
    with open("sql/initSql.sql", "r", encoding="utf8") as f:
        execute_sql_file(f)


def init_sql():
    with open("sql/initData.sql", 'r', encoding='utf8') as f:
        execute_sql_file(f)


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


def get_dept_id(dept_name):
    conn = get_db()
    cursor = conn.cursor()
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]


def get_user_id(username):
    conn = get_db()
    cursor = conn.cursor()
    select_sql = "SELECT user_id FROM employee WHERE username = %s"
    cursor.execute(select_sql, (username,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(username))
    return row[0]


def get_user_name(user_id):
    conn = get_db()
    cursor = conn.cursor()
    select_sql = "SELECT name FROM employee WHERE user_id = %s"
    cursor.execute(select_sql, (user_id,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(user_id))
    return row[0]


if __name__ == '__main__':
    init_db()
    init_tables()
    init_sql()
    init_data.init_data()
