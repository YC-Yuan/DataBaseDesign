# leader 后端服务

from flask import Blueprint, request
from dao import dao_user, dao_employee, dao_course
from modules import route

bp_leader = Blueprint('leader', __name__, url_prefix='/leader')


# 用员工号查成绩
@bp_leader.route('/employee/score', methods=['GET'])
def score():
    uid = request.values.get('uid')
    return route.staff(user_id=uid)
