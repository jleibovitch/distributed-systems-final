from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
# A key for protection of outsiders editing or viewing data
app.config['SECRET_KEY'] = '6551817c95c0b084a5a9aceaab30db56'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# defining certain things
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from . import routes

routes.start_client()
