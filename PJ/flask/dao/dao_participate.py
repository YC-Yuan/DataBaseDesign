from constants.info import *
from dao import dao_user, dao_core, dao_log
import pymysql as sql
import utils


def get_tests_by_uc(user_id, course_id):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
        cmd = 'select score,time from participate ' \
              'where user_id= %s and course_id=%s'
        cursor.execute(cmd, (user_id, course_id))
        res = cursor.fetchall()
        tests = []
        for r in res:
            tests.append({
                'score': r[0],
                'time': r[1],
            })
        return tests
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#   录入成绩
def score_input(instructor_username, user_id, course_id, score):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    try:
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
            operation = "input score %s for %s on %s" % (score, user_id, course_id)
            log_sql = dao_log.insert_log(instructor_username, operation)
            cursor.execute(log_sql)
            conn.commit()
            return True
        else:
            raise sql.MySQLError("尚未结课")
    except sql.MySQLError as e:
        print(e)
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
