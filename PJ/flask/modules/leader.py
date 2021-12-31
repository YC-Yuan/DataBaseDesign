# leader 后端服务

from flask import Blueprint, request
from dao import dao_user, dao_employee, dao_course, dao_staff
from modules import route
import pymysql as sql

bp_leader = Blueprint('leader', __name__, url_prefix='/leader')


# 用员工号查成绩
@bp_leader.route('/employee/score', methods=['GET'])
def score():
    uid = request.values.get('uid')
    return route.staff(user_id=uid)


# 员工转部门
@bp_leader.route('/employee/change_dept', methods=['POST'])
def change_dept():
    lid = request.values.get('leader_id')
    leader_username = dao_user.get_username(lid)
    uid = request.values.get('uid')
    dept = request.values.get('dept')
    try:
        dao_staff.transfer_dept(username=leader_username, user_id=uid, dept_name=dept)
    except sql.MySQLError as e:
        print(e)
        return "出错了"
    return "成功"
