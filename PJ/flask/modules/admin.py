from flask import Blueprint, request, jsonify
from dao import dao_user, dao_staff, dao_course, dao_dept, dao_employee
from modules import route
import pymysql as sql

bp_admin = Blueprint('admin', __name__, url_prefix='/admin')


@bp_admin.route('/create/course', methods=['post'])
def create_course():
    username = request.values.get('admin')
    i_name = request.values.get('instructor')
    instructor = dao_employee.get_employee_by_name(i_name)
    if instructor is None:
        return "教员名字错误"
    cid = request.values.get('course_id')
    name = request.values.get('name')
    content = request.values.get('content')
    category = request.values.get('category')
    start_time = request.values.get('start_time')
    end_time = request.values.get('end_time')
    dao_course.insert_course(username, instructor['user_id'], cid, name, content, category, start_time, end_time)
    return route.admin(username)


@bp_admin.route('/create/employee', methods=['post'])
def create_employee():
    admin = request.values.get('admin')
    username = request.values.get('username')
    pwd = request.values.get('pwd')
    user_id = request.values.get('user_id')
    name = request.values.get('name')
    gender = request.values.get('gender')
    age = request.values.get('age')
    hire_date = request.values.get('hire_date')
    city = request.values.get('city')
    telephone = request.values.get('telephone')
    email = request.values.get('email')
    dept_name = request.values.get('dept_name')
    # 员工 教员 部门主管
    role = request.values.get('role')
    dao_employee.insert_employee(username=username, pwd=pwd, user_id=user_id,
                                 name=name, gender=gender, age=age,
                                 hire_date=hire_date, city=city, telephone=telephone,
                                 email=email, dept_name=dept_name, role=role)
    return route.admin(admin)
