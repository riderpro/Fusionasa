from datetime import datetime
from datetime import date
from pack import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique = True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	email = db.Column(db.String(30), unique=True)
	phone = db.Column(db.Integer, unique=True, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):  # magic method
		return "User('{self.username}','{self.date_posted}','{self.email}','{self.phone}')"


class Feedback(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(20), nullable=False)
	lname = db.Column(db.String(20), nullable=False)
	country = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(30), unique=True)
	message = db.Column(db.String(20), nullable=False)

	def __repr__(self):  # magic method
		return "Feedback('{self.fname}','{self.lname}','{self.country}','{self.email}','{self.message}')"
