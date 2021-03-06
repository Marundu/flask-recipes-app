from flask_wtf import Form
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class EmailForm(Form):
    email=StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=40)])

class LoginForm(Form):
    email=StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=40)])
    password=PasswordField('Password', validators=[DataRequired()])
    #remember_me=BooleanField('Remember Me?', default=False)    

class PasswordForm(Form):
    password=PasswordField('Password', validators=[DataRequired()])
    confirm=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class RegisterForm(Form):
    email=StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=40)])
    password=PasswordField('Password', validators=[DataRequired(), Length(min=8, max=40)])
    confirm=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
