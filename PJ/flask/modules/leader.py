# leader 后端服务

from flask import Blueprint, request, jsonify
from dao import dao_user, dao_staff, dao_course
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


@bp_leader.route('/search/course_name', methods=['POST'])
def search_by_course_name():
    dept_name = request.values.get('dept_name')
    name = request.values.get('course_name')
    course = dao_course.get_course_by_name(name)
    if course is None:
        return "课程不存在"
    evaluation = request.values.get('evaluation')
    if evaluation == "":
        evaluation = None
    res = dao_staff.search_by_course_and_evaluation(dept_name, course['course_id'], False, evaluation)
    return jsonify(res)


# def search_by_test(dept_name, course_id, is_fail, num, compare):

@bp_leader.route('/search/test', methods=['POST'])
def search_by_test():
    dept_name = request.values.get('dept_name')
    name = request.values.get('course_name')
    course = dao_course.get_course_by_name(name)
    if course is None:
        return "课程不存在"
    is_fail = request.values.get('is_fail') == "fail"
    num = request.values.get('num')
    compare = request.values.get('compare')
    res = dao_staff.search_by_test(dept_name, course['course_id'], is_fail, int(num), compare)
    return jsonify(res)
