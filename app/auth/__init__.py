from flask import Blueprint, g, session, request, url_for, render_template, redirect, flash, get_flashed_messages

from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm

from functools import wraps
from datetime import datetime

bp = Blueprint('auth', __name__)


def login_required(view):
	""" Decorator that redirects to login screen if auth is needed """
	@wraps(view)
	def wrapped_view(*args, **kwargs):
		if not g.user:
			flash("You must be logged in to view this page.")
			return redirect((url_for('auth.login')))
		return view(*args, **kwargs)
	return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():
	""" Login function validates user info with info in database """
	
	form = LoginForm()

	if request.method == 'POST' and form.validate():
		user = User.query.filter_by(email=form.email.data).first()

		if not user or not user.checkPassword(form.password.data):
			flash('Email/Password incorrect. Try again.')
			return redirect(url_for('auth.login'))
		else:
			session.clear()
			session['id'] = user.id
			session.permanent = form.remember.data
			flash("Welcome g.user.username!")
			return redirect(url_for('main.index'))
	return render_template('auth/login.html', title='login', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()

	if request.method=='POST' and form.validate():
		user = User.create(username=form.username.data, email=form.email.data)
		user.setPassword(form.password.data)
		db.session.commit()
		flash("Thanks for registering!")
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
	session.clear()
	g.user = None
	flash("Logout successful.")
	return redirect(url_for('auth.login'))


@bp.before_app_request
def save_user_session():
	""" Saves user in context variable for easy access. """

	uId = session.get('id')
	if not uId:
		g.user = None
	else:
		g.user = User.query.filter_by(id=uId).first()