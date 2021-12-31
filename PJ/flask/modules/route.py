from flask import Blueprint, render_template
from dao import dao_core, dao_dept, dao_course, dao_staff, dao_employee, dao_leader, dao_participate

bp_route = Blueprint('route', __name__, url_prefix="")


# 所有render在此实现

@bp_route.route('/', methods=['GET'])
def home():
    return render_template('login.html')


@bp_route.route('/login', methods=['GET'])
def login():
    return home()


def login_failed(msg):
    return render_template('login.html', msg=msg)


# 获取员工信息传给前端
def staff(user_id):
    # 查找个人信息
    info = dao_staff.get_user_info(user_id)
    # 查找课程与教员
    courses = dao_course.get_course_by_uid(user_id)
    for course in courses:
        best_score = dao_participate.get_best_score(user_id, course['course_id'])
        course['score'] = best_score
    # 查找历史上课信息
    history = dao_course.get_course_history_by_uid(user_id)
    return render_template('staff.html',
                           info=info, courses=courses, history=history)


def instructor(user_id):
    instructor = dao_employee.get_employee_by_uid(user_id=user_id)
    courses = dao_course.get_courses_by_instructor(instructor_id=user_id)
    for course in courses:
        # 添加学生和最高得分
        course_id = course['course_id']
        students = dao_staff.get_staff_by_course_id(course_id=course_id)
        for student in students:
            best_score = dao_participate.get_best_score(student['user_id'], course_id)
            student['score'] = best_score
        course['students'] = students
    return render_template('instructor/instructor.html', instructor=instructor, courses=courses)


def leader(user_id):
    dept = dao_leader.get_dept_by_leader(user_id)
    # 查找所管理部门员工信息
    employee = dao_employee.get_employee_by_dept(dept=dept)
    # 查找所管理部门课程信息
    courses = dao_course.get_course_by_dept_name(dept_name=dept)
    # 查找符合转部门情况的员工信息
    qualified_employee = dao_dept.get_qualified_staff(dept_name=dept)
    return render_template('leader/leader.html', uid=user_id,
                           dept_name=dept, employee=employee, courses=courses,
                           qualified_employee=qualified_employee)


def admin(username):
    return render_template('admin/admin.html')
