from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db, RegisterUser
from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://root:@localhost/login')
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

		if image:
			filename = image.filename
			file_path = os.path.join('images', filename)
			image.save(file_path)

		print email, password, verify
		new_user = RegisterUser(email=email, password=password, profile_pic=file_path)
		db.session.add(new_user)
		db.session.commit()

		db_user = RegisterUser.query.filter_by(email = email).first()

    	return render_template("success.html", email=db_user.email, pic=db_user.profile_pic)

@app.route('/login')
def login():
    return render_template("login.html") 

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
	app.debug = True
	app.run()    