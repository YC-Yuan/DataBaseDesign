from flask import Blueprint, request, jsonify
from dao import dao_user, dao_staff, dao_course, dao_dept, dao_employee
from modules import route
import pymysql as sql

bp_admin = Blueprint('admin', __name__, url_prefix='/admin')


# 课程管理接口-创建/修改(根据是否已有自动选择) 删除
@bp_admin.route('/create/course', methods=['post'])
def create_course():
    # 参数解析
    username = request.values.get('admin')
    i_name = request.values.get('instructor')
    cid = request.values.get('course_id')
    instructor = dao_employee.get_employee_by_name(i_name)
    name = request.values.get('name')
    content = request.values.get('content')
    category = request.values.get('category')
    start_time = request.values.get('start_time')
    end_time = request.values.get('end_time')
    # 参数检验
    if instructor is None:
        return "教员名字错误"
    # 根据是否有课选择操作
    if dao_course.has_course(cid):
        # 修改课程
        dao_course.set_course(username, instructor['user_id'], cid, name, content, category, start_time, end_time)
    else:
        # 新建课程
        dao_course.insert_course(username, instructor['user_id'], cid, name, content, category, start_time, end_time)
    return route.admin(username)


@bp_admin.route('/delete/course', methods=['post'])
def delete_course():
    username = request.values.get('admin')
    cid = request.values.get('course_id')
    # 检测是否存在
    if not dao_course.has_course(cid):
        return "没有该课程"
    dao_course.delete_course(username, cid)
    return route.admin(username)


# 员工管理接口-创建 删除 修改
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


@bp_admin.route('/delete/employee', methods=['post'])
def delete_employee():
    admin = request.values.get('admin')
    username = request.values.get('username')
    dao_user.delete_employee(username)
    return route.admin(admin)


# 修读要求接口
@bp_admin.route('course/need',methods=['POST'])
def need():
    admin = request.values.get('admin')
    course_id = request.values.get('course_id')
    dept = request.values.get('dept')
    needy = request.values.get('needy')
    if not dao_course.has_course(course_id):
        return "课程编号不存在"
    if not dao_dept.has_dept(dept):
        return "部门不存在"
    dao_course.set_course_require(admin, course_id, dept, needy)
    return route.admin(username=admin)
