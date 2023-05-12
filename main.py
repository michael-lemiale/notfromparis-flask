import os

from datetime import datetime
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, url_for, flash

# load env vars
load_dotenv()

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)

# connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_PG', 'sqlite:///notfromparis.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# configure models for db
class EmailResponse(db.Model):
    __tablename__ = 'email_responses'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    time_created = db.Column(db.DateTime(), default=datetime.utcnow)

@app.route('/')
def home():
    # render home page
    return render_template('index.html')

@app.route('/bio')
def bio():
    # render bio page
    return render_template('bio.html')   

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # get email from form and create db record
        new_email_response = EmailResponse(email = request.form.get('email'))        
        # commit to db
        db.session.add(new_email_response)
        db.session.commit()
        # thank you message
        flash("WELCOME,we're glad you're here")
        # return home page
        return redirect(url_for('home'))
    # if this errors for any reason, return to home page
    return render_template('index.html') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
