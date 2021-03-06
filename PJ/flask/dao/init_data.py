from dao.dao_employee import *
from dao.dao_course import *
from dao.dao_core import *
from dao.config import *


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


def init_tables():
    with open("sql/initSql.sql", "r", encoding="utf8") as f:
        execute_sql_file(f)


def init_sql():
    with open("sql/initData.sql", 'r', encoding='utf8') as f:
        execute_sql_file(f)


def init_data():
    insert_employee('18307110072', 'password', '18307110072', '赵书誉', '男', 22, '2018-9-10', '上海', '13681981193',
                    '2011710343@qq.com', '策划部门', LEADER, '2020-3-15')
    insert_employee('19302010020', 'password', '19302010020', '袁逸聪', '男', 20, '2019-9-10', '深圳', '13651085108',
                    '19302010020@fudan.edu.com', '开发部门', LEADER, '2020-3-15')
    insert_employee('19302011478', 'password', '19302011478', '李耀', '男', 22, '2019-9-10', '上海', '13658258515',
                    '19302011478@fudan.edu.com', '策划部门', INSTRUCTOR, '2020-3-15')
    insert_employee('19302012545', 'password', '19302012545', '王鑫', '女', 30, '2019-9-10', '上海', '18611767887',
                    '19302012545@fudan.edu.com', '开发部门', INSTRUCTOR, '2020-3-15')
    insert_employee('19302013589', 'password', '19302013589', '王倩', '男', 28, '2015-9-10', '上海', '13626976926',
                    '19302013589@fudan.edu.com', '策划部门')
    insert_employee('19302014085', 'password', '19302014085', '卢潇', '女', 21, '2017-9-10', '上海', '13696022992',
                    '19302014085@fudan.edu.com', '策划部门')
    insert_employee('19302015821', 'password', '19302015821', '宋雪', '男', 25, '2008-9-10', '上海', '13602825925',
                    '19302015821@fudan.edu.com', '开发部门')
    insert_employee('19302016764', 'password', '19302016764', '蒋玥', '女', 41, '2008-9-10', '上海', '13104718946',
                    '19302016764@fudan.edu.com', '开发部门')
    insert_employee('19302017321', 'password', '19302017321', '雪灵灵', '女', 34, '2019-9-10', '上海', '13610951833',
                    '19302017321@fudan.edu.com', '开发部门')
    insert_employee('19302018754', 'password', '19302018754', '茄子', '女', 22, '2020-9-10', '上海', '18981981193',
                    '19302018754@fudan.edu.com', '开发部门')
    insert_course(ADMIN_USERNAME, '19302011478', '33160', '手游策划', '薅玩家羊毛', '策划', '2020-5-17', '2020-12-08')
    insert_course(ADMIN_USERNAME, '19302012545', '35142', '数据库设计', '数据库设计', '开发', '2021-3-10', '2021-7-18')
    insert_course(ADMIN_USERNAME, '19302012545', '35155', '软件测试', '软件测试', '测试', '2021-7-12', '2021-12-31')
    set_course_require(ADMIN_USERNAME, '33160', '策划部门', MANDATORY)
    set_course_require(ADMIN_USERNAME, '35142', '开发部门', MANDATORY)
    set_course_require(ADMIN_USERNAME, '35142', '策划部门', OPTIONAL)
    set_course_require(ADMIN_USERNAME, '35155', '开发部门', OPTIONAL)
    update_courses_state()


if __name__ == '__main__':
    init_db()
    init_tables()
    init_sql()
    init_data()
