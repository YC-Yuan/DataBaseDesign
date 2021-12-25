from flask import Blueprint, render_template
import pymysql as sql

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


def staff():
    return render_template('/staff.html')


def instructor():
    return render_template('/instructor')


def leader():
    return render_template('/leader.html')


def admin():
    return render_template('/admin.html')
