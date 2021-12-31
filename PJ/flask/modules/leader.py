# leader 后端服务

from flask import Blueprint, request, jsonify
from dao import dao_user, dao_staff
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


@bp_leader.route('/search/category', methods=['POST'])
def search_by_category():
    dept_name = request.values.get('dept_name')
    category = request.values.get('category')
    evaluation = request.values.get('evaluation')
    if evaluation == "":
        evaluation = None
    res = dao_staff.search_by_course_and_evaluation(dept_name, category, True, evaluation)
    return jsonify(res)


@bp_leader.route('/search/course_id', methods=['POST'])
def search_by_course_id():
    dept_name = request.values.get('dept_name')
    category = request.values.get('course_id')
    evaluation = request.values.get('evaluation')
    if evaluation == "":
        evaluation = None
    res = dao_staff.search_by_course_and_evaluation(dept_name, category, False, evaluation)
    return jsonify(res)
