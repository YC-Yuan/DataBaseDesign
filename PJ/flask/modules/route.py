from flask import Blueprint, render_template
from dao import dao_core, dao_course, dao_staff, dao_employee, dao_leader

bp_route = Blueprint('route', __name__, url_prefix="")


# 所有render在此实现

@bp_route.route('/', methods=['GET'])
def home():
    return render_template('/login.html')


@bp_route.route('/login', methods=['GET'])
def login():
    return home()


def login_failed(msg):
    return render_template('/login.html', msg=msg)


# 获取员工信息传给前端
def staff(user_id):
    # 查找个人信息
    info = dao_staff.get_user_info(user_id)
    # 查找课程与教员
    courses = dao_course.get_course_by_uid(user_id)
    # 查找历史上课信息
    history = dao_course.get_course_history_by_uid(user_id)
    return render_template('/staff.html',
                           info=info, courses=courses, history=history)


def instructor(user_id):
    return render_template('/instructor')


def leader(user_id):
    dept = dao_leader.get_dept_by_leader(user_id)
    # 查找所管理部门员工信息
    employee = dao_employee.get_employee_by_dept(dept=dept)
    # 查找所管理部门课程信息
    courses = dao_course.get_course_by_dept(dept=dept)
    return render_template('/leader.html',
                           employee=employee, courses=courses)


def admin(username):
    return render_template('/admin.html')
