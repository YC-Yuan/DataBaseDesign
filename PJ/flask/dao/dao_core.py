import pymysql as sql

from dao import init_data
from dao.config import *
import dao.init_data


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


# 执行无返回的sql语句
def execute_sql(cmd):
    conn = get_db()
    cursor = conn.cursor()
    try:
        print("执行无返回的sql语句:%s" % cmd)
        cursor.execute(cmd)
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# 批量执行无返回的sql语句
def execute_sql_list(cmd_list):
    conn = get_db()
    cursor = conn.cursor()
    try:
        print("执行无返回的sql list")
        for cmd in cmd_list:
            print("执行无返回的sql语句:%s" % cmd)
            cursor.execute(cmd)
        print("list执行完毕")
        conn.commit()
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
        exit(0)
    finally:
        cursor.close()
        conn.close()


def execute_sql_file(f):
    sql_list = f.read().split(';')[:-1]
    execute_sql_list(sql_list)


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


if __name__ == '__main__':
    init_db()
    init_tables()
    init_sql()
    init_data.init_data()
