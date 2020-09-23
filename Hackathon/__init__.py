from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from functools import wraps
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
import os, json

app = Flask(__name__, instance_path='/protected', instance_relative_config=True)
app.config['SECRET_KEY'] = '47c4609da2d63b06e8bb8ed2cf93af00'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['protected'] = 'protected'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bạn cần phải đăng nhập trước'
login_manager.login_message_category = 'danger'

contestData = json.load(open('Hackathon/contest.json'))

from Hackathon import routes
from Hackathon.models import User, Post, Submission

class AdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.username in ["TeamHackathon2020", "kurone02"])

class CustomView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.username in ["TeamHackathon2020", "kurone02"])

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập đường dẫn này!', 'danger')
        return redirect(url_for('login'))

admin = Admin(app, index_view=AdminIndexView())
admin.add_view(CustomView(User, db.session))
admin.add_view(CustomView(Post, db.session))
admin.add_view(CustomView(Submission, db.session))