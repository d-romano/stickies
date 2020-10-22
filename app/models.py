"""Data Models"""
from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class BaseMixin(object):
	""" Handles common functions shared between models. """
	@classmethod
	def create(cls, **kw):
		""" Adds a record into table that calls function """
		obj = cls(**kw)
		db.session.add(obj)
		db.session.commit()
		return obj


class User(BaseMixin, db.Model):
	""" Model for users """
	
	id = db.Column(
		db.Integer(),
		primary_key=True
	)
	username = db.Column(
		db.String(120),
		unique=True,
		index=True,
		nullable=False
	)
	email = db.Column(
		db.String(120),
		unique=True,
		index=True,
		nullable=False
	)
	passHash = db.Column(
		db.String(120)
	)
	notes = db.relationship(
		'Note', 
		backref='user',
		lazy=True
	)

	def __repr__(self):
		return '<User %r>' % self.username

	def setPassword(self, unhashPass):
		""" Generate and store hash for passed password value. """
		self.passHash = generate_password_hash(unhashPass)

	def checkPassword(self, unhashPass):
		""" Ensures that stored hash matches hash entered password. """
		return check_password_hash(self.passHash, unhashPass)


class Note(BaseMixin, db.Model):
	""" Model for notes"""

	id = db.Column(
		db.Integer(),
		primary_key=True
	)
	title= db.Column(
		db.String(50),
		nullable=False,
		index=True
	)
	body = db.Column(
		db.String(255),
	)
	created = db.Column(
		db.DateTime(),
		default=datetime.utcnow()
	)
	modified = db.Column(
		db.DateTime(),
		nullable=True
	)
	userId = db.Column(
		db.Integer(),
		db.ForeignKey('user.id'),
		nullable=False
	)
	def __repr__(self):
		return '<Post %r>' % self.title