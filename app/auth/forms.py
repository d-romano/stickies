from app import db
from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email, ValidationError

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired(message='Please enter password')])
	remember = BooleanField("Remember Me")
	submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[InputRequired(), Length(max=120)])
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired(), Length(max=25),
		EqualTo('repeat', message='Passwords Must Match.')])
	repeat = PasswordField('Repeat Password', validators=[InputRequired()])
	submit = SubmitField('Register')


	def validate_email(self, email):
		''' Checks db for existing email. '''
		user = User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError("Email already in use, please select another one.")


	def validate_username(self, username):
		''' Checks db for existing username. '''
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("Username already in use, please select another one.")

