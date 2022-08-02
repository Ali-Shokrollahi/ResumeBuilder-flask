from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
FLASK_APP='__init__.py'

file_dir = os.path.dirname(__file__)
goal_route = os.path.join(file_dir, "app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + goal_route
app.config["SECRET_KEY"] = "123456"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import model
from . import view

if __name__ == '__main__':
    app.run()
