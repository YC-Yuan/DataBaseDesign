from constants.info import *
import pymysql as sql
from dao.dao_core import *
import utils


''' 教师相关功能 '''


#   录入成绩
def score_input(instructor_id, user_id, course_id, score):
    try:
        conn = get_db()
        cursor = conn.cursor()
        __check_course(cursor, instructor_id, course_id)
        select_sql = "SELECT end_time FROM course WHERE course_id = %s"
        cursor.execute(select_sql, (course_id,))
        row = cursor.fetchone()
        if utils.check_course_end(row[0]):
            select_sql = "SELECT evaluation FROM take WHERE user_id = %s AND course_id = %s"
            cursor.execute(select_sql, (user_id, course_id,))
            eva = cursor.fetchone()[0]
            if eva == PASSED:
                raise sql.MySQLError("禁止卷逼刷分")
            insert_sql = "INSERT INTO participate VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_sql, (user_id, course_id, utils.get_current_timestamp(), score,))
            #   及格则自动修改状态
            if score >= PASS_LINE:
                update_sql = "UPDATE take SET evaluation = %s WHERE user_id = %s AND course_id = %s"
                cursor.execute(update_sql, (PASSED, user_id, course_id,))
            conn.commit()
            print("score_input " + str(user_id) + " " + str(course_id) + " " + str(score))
        else:
            raise sql.MySQLError("尚未结课")
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


#   检查教师权限
def __check_course(cursor, instructor_id, course_id):
    select_sql = "SELECT COUNT(*) FROM course WHERE course_id = %s AND instructor_id = %s"
    cursor.execute(select_sql, (course_id, instructor_id,))
    if cursor.fetchone()[0] == 0:
        raise sql.MySQLError("没有权限")
