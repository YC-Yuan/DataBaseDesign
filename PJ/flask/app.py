from flask import Flask
from flask_bootstrap import Bootstrap

from modules import route

app = Flask(__name__)

app.register_blueprint(route.bp_route)

bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run()
