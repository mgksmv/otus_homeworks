from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length


class SingUpForm(FlaskForm):
    username = StringField('Username *', validators=[DataRequired(), Length(6, 32)])
    email = EmailField('Email *', validators=[DataRequired(), Length(6, 32)])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    bio = TextAreaField('Bio')
    password_1 = PasswordField('Password *', validators=[DataRequired(), Length(6, 32)])
    password_2 = PasswordField('Repeat password *', validators=[DataRequired(), Length(6, 32)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(6, 32)])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    bio = TextAreaField('Bio')
    email = EmailField('Email', validators=[DataRequired(), Length(6, 32)])
    password = PasswordField('Password')


class ResetEmailForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(min=6, max=32)])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])


class CreateSuperUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(6, 32)])
    email = EmailField('Email', validators=[DataRequired(), Length(6, 32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 32)])
