from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:@localhost/login'
db = SQLAlchemy(app)

manager = Manager(app)


class RegisterUser(db.Model):

	__tablename__ = 'RegisterUser'
	user_id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String)
	password = db.Column(db.String)
	profile_pic = db.Column(db.String)

	def __init__(self, email, password, profile_pic):
		self.email = email
		self.password = password
		self.profile_pic = profile_pic

if __name__ == "__main__":
	manager.run()		
