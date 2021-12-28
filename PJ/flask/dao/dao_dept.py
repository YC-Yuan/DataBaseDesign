import pymysql as sql
import dao.dao_core as dao_core


def get_dept_id(dept_name):
    conn = dao_core.get_db()
    cursor = conn.cursor()
    select_sql = "SELECT dept_id FROM department WHERE name = %s"
    cursor.execute(select_sql, (dept_name,))
    row = cursor.fetchone()
    if row is None:
        raise sql.MySQLError("{} does not exist".format(dept_name))
    return row[0]
