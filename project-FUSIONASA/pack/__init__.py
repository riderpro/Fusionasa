from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY']='12fe195cde45bcea3aec933078687856'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
login_manager = LoginManager(app)
import pack.routes