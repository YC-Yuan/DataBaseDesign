import pymysql as sql

configs = []

with open("configs.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        configs.append(line)


# 获取数据库连接 如果没有库则创建
def get_db():
    sql_create_db = 'create database if not exists ' + configs[4]
    try:
        db = sql.connect(host=configs[0],
                         port=3306,
                         user=configs[2],
                         password=configs[3])
        cursor = db.cursor()
        cursor.execute(sql_create_db)
        cursor.close()
        db.close()
        return sql.connect(host=configs[0],
                           port=3306,
                           user=configs[2],
                           password=configs[3],
                           database=configs[4])
    except sql.MySQLError as e:
        print(e)
        print("数据库连接失败,请检查configs.txt\n4行分别表示主机地址,mysql用户名,mysql密码,mysql中指定database")
        exit(0)


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


if __name__ == '__main__':
    init_tables()
