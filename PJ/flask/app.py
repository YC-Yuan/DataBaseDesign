from flask import Flask
from flask_bootstrap import Bootstrap

from modules import route, user, leader

app = Flask(__name__)

app.register_blueprint(route.bp_route)
app.register_blueprint(user.bp_user)
app.register_blueprint(leader.bp_leader)

bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run()
