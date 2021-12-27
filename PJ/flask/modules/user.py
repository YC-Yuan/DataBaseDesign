# user 后端服务

from flask import Blueprint, request
from dao import dao_user, dao_employee
from modules import route

bp_user = Blueprint('user', __name__, url_prefix="/user")


@bp_user.route('/login', methods=['POST'])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    if dao_user.has_user(username, password):
        # 登录成功
        if dao_user.is_admin(username):
            return route.admin(username)
        user_id = dao_user.get_user_id(username)
        if dao_user.is_leader(user_id):
            return route.leader(user_id)
        if dao_user.is_staff(user_id):
            return route.staff(user_id)
        if dao_user.is_instructor(user_id):
            return route.instructor(user_id)
    else:
        # 登录失败
        return route.login_failed(msg="用户名或密码错误")


@bp_user.route('/info_modify', methods=['POST'])
def info_modify():
    user_id = request.values.get('user_id')
    city = request.values.get('city')
    telephone = request.values.get('telephone')
    email = request.values.get('email')
    dao_employee.modify_info(user_id=user_id, city=city, telephone=telephone, email=email)
    return route.staff(user_id)
