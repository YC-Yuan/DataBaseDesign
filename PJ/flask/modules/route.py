from flask import Blueprint, render_template
from dao import dao_staff
from dao import dao

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
    courses = []
    course = {
        'name': '数据库设计',
        'content': '设计数据库',
        'category': '计算机',
        'start_time': '2021-19-12',
        'end_time': '2034-12-21',
        'instructor': '毅宝',
    }
    courses.append(course)
    # 查找历史上课信息
    history = []
    history.append({
        'name': '软件实践',
        'content': '实践软件',
        'category': '计算机',
        'start_time': '2018-1-12',
        'end_time': '2019-12-21',
        'instructor': '毅宝',
        'evaluation': '通过',
        'tests': [{
            'time': '2019-12-22',
            'score': 50
        }, {
            'time': '2019-12-23',
            'score': 80
        }, ]
    })
    return render_template('/staff.html',
                           info=info, courses=courses, history=history)


def instructor(user_id):
    return render_template('/instructor')


def leader(user_id):
    return render_template('/leader.html')


def admin(username):
    return render_template('/admin.html')
