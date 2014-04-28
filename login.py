from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db, RegisterUser
from flask import Flask, render_template, request
import os

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://suraj:wilshere10@localhost/login')
app.config['SQLALCHEMY_DATABASE_URI'] = engine

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	else:
		email = request.form.get("email")
		password = request.form.get("password")
		verify = request.form.get("verify")
		image = request.files["profile_pic"]
		print email, password, verify, image
    	return render_template("success.html")

@app.route('/login')
def login():
    return render_template("login.html") 

if __name__ == "__main__":
	app.debug = True
	app.run()    