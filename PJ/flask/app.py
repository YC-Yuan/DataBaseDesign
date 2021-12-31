from flask import Flask
from flask_bootstrap import Bootstrap

from modules import route, user, leader, instructor

app = Flask(__name__)

app.register_blueprint(route.bp_route)
app.register_blueprint(user.bp_user)
app.register_blueprint(leader.bp_leader)
app.register_blueprint(instructor.bp_instructor)

bootstrap = Bootstrap(app)

app.config['JSON_AS_ASCII'] = False

if __name__ == '__main__':
    app.run()
