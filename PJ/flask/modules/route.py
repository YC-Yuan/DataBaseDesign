from flask import Blueprint, render_template

bp_route = Blueprint('route', __name__)


# 所有render在此实现

@bp_route.route('/', methods=['GET'])
def home():
    return render_template('/login.html')


@bp_route.route('/login', methods=['GET'])
def login():
    return render_template('/login.html')
