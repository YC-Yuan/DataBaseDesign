import pymysql as sql
from dao.config import *


def init_db():
    sql_create_db = 'create database if not exists ' + DB_NAME
    db = sql.connect(host=HOST,
                     port=3306,
                     user=USER,
                     password=PWD)
    cursor = db.cursor()
    cursor.execute(sql_create_db)
    cursor.close()
    db.close()


def init_tables():
    db = get_db()
    cursor = db.cursor()
    try:
        with open("./InitSql.sql", "r", encoding="utf8") as f:
            sql_list = f.read().split(';')[:-1]
            for x in sql_list:
                if '\n' in x:
                    # 脚本换行处替换为空格
                    x = x.replace('\n', ' ')
                x += ';'
                cursor.execute(x)
    except sql.MySQLError as e:
        print(e)
        db.rollback()
        print("""建表出错,请检查init_tables函数""")
        exit(0)
    finally:
        cursor.close()
        db.close()


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


def get_dept_id(cursor, dept_name):
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]


if __name__ == '__main__':
    init_db()
    init_tables()
