from flask import Blueprint, render_template

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
def staff(username):
    # 查找个人信息
    info = dict()
    info['user_id'] = 19302010020
    info['name'] = '袁逸聪'
    info['geder'] = '男'
    info['age'] = 20
    info['hire_date'] = '2021 - 19 - 21'
    info['city'] = '深圳'
    info['telephone'] = 15001933144
    info['email'] = '1534401580@qq.com'
    # 查找课程与教员
    courses = []
    course = {
        'name': '数据库设计',
        'content': '设计数据库',
        'category': '计算机',
        'start_time': '2021-19-12',
        'end_time': '2034-12-21',
        'instructor': '毅宝',
        'department': '计算机开发部',
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
        'department': '计算机开发部',
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


def instructor():
    return render_template('/instructor')


def leader():
    return render_template('/leader.html')


def admin():
    return render_template('/admin.html')
