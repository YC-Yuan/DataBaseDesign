# instructor 后端服务

from flask import Blueprint, request
from dao import dao_participate, dao_employee, dao_course
from modules import route
import pymysql as sql

bp_instructor = Blueprint('instructor', __name__, url_prefix='/instructor')


@bp_instructor.route('/score', methods=['POST'])
def score():
    iid = request.values.get('instructor_id')
    instructor = dao_employee.get_employee_by_uid(iid)
    if instructor is None:
        return "身份信息错误"
    i_username = instructor['username']
    c_name = request.values.get('course')
    course = dao_course.get_course_by_name(c_name)
    if course is None:
        return "课程不存在"
    sid = request.values.get('student_id')
    student = dao_employee.get_employee_by_uid(sid)
    if student is None:
        return "查无此人"
    score = request.values.get('score')
    code, msg = dao_participate.score_input(i_username, sid, course['course_id'], score)
    if code:
        return route.instructor(iid)
    else:
        return msg
