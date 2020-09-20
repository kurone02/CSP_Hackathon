from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Hackathon import bcrypt
from Hackathon.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired(message="Tài khoản không thể rỗng"), Length(min=2, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(message="Mật khẩu không thể rỗng")])
    confirm_password = PasswordField('Nhập lại mật khẩu', validators=[DataRequired(message="Vui lòng xác nhận mật khẩu"), EqualTo('password', message="Mật khẩu không khớp")])
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tài khoản đã tồn tại!')

class LoginForm(FlaskForm):
    username = StringField('Tài khoản', validators=[DataRequired(message="Hãy nhập tài khoản"), Length(min=2, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(message="Hãy nhập mật khẩu")])
    submit = SubmitField('Đăng nhập')

class UpdateAccountForm(FlaskForm):
    current_password = PasswordField('Mật khẩu cũ', validators=[DataRequired(message="Hãy nhập mật khẩu cũ")])
    new_password = PasswordField('Mật khẩu mới', validators=[DataRequired(message="Mật khẩu mới không thể rỗng")])
    confirm_password = PasswordField('Nhập lại mật khẩu mới', validators=[DataRequired(message="Vui lòng xác nhận mật khẩu mới"), EqualTo('new_password', message="Mật khẩu không khớp")])
    submit = SubmitField('Cập nhật')

    def validate_current_password(self, current_password):
        if ((not current_user.repass) and current_user.password != current_password.data) \
        or (current_user.repass and (not bcrypt.check_password_hash(current_user.password, current_password.data))):
            raise ValidationError('Mật khẩu cũ không chính xác')

    def validate_new_password(self, new_password):
        if ((not current_user.repass) and current_user.password == new_password.data) \
        or (current_user.repass and bcrypt.check_password_hash(current_user.password, new_password.data)):
            raise ValidationError('Mật khẩu mới phải khác mật khẩu cũ')

class PostForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired()])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    submit = SubmitField('Đăng bài')