from constants.info import *
from dao.dao_core import *
from dao import dao_user
import utils


# 根据uid搜索员工所选课程
def get_course_by_uid(user_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cmd = 'select course_id,name,content,category,start_time,end_time,instructor_id ' \
              'from course natural join (' \
              'select * from take ' \
              'where take.user_id = %s) as t'
        cursor.execute(cmd, user_id)
        res = cursor.fetchall()
        courses = []
        for r in res:
            ins_id = r[6]
            ins_name = dao_user.get_user_name(ins_id)
            courses.append({
                'cid': r[0],
                'name': r[1],
                'content': r[2],
                'category': r[3],
                'start_time': r[4],
                'end_time': r[5],
                'instructor': ins_name,
            })
        return courses
    except sql.MySQLError as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
