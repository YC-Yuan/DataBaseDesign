# user 后端服务

from flask import Blueprint, request
from dao import dao
from dao import dao_user
from modules import route

bp_user = Blueprint('user', __name__, url_prefix="/user")


@bp_user.route('/login', methods=['POST'])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    return route.staff('yyc')
    if dao_user.has_user(username, password):
        # 登录成功
        if dao_user.is_admin(username):
            return route.admin()
        user_id = dao.get_user_id(username)
        if dao_user.is_leader(user_id):
            return route.leader()
        if dao_user.is_staff(user_id):
            return route.staff()
        if dao_user.is_instructor(user_id):
            return route.instructor()
    else:
        # 登录失败
        return route.login_failed(msg="用户名或密码错误")
