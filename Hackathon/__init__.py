from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from functools import wraps
import os, json

app = Flask(__name__)
app.config['SECRET_KEY'] = '47c4609da2d63b06e8bb8ed2cf93af00'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bạn cần phải đăng nhập trước'
login_manager.login_message_category = 'danger'

contestData = json.load(open('Hackathon/contest.json'))

from Hackathon import routes