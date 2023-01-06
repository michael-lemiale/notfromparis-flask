import os

from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# app config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_PG', 'sqlite:///grail.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# configure models
class Response(db.Model):
    __tablename__ = 'responses'
