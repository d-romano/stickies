from app import db

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email

class LoginForm(FlaskForm):

	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired(message='Please enter password')])
	submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[InputRequired(), Length(max=120)])
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired(), Length(max=25),
		EqualTo('repeat', message='Passwords Must Match.')])
	repeat = PasswordField('Repeat Password', validators=[InputRequired()])
	submit = SubmitField('Register')
