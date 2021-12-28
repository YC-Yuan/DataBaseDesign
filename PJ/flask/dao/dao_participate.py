from constants.info import *
from dao import dao_user, dao_core, dao_dept
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
