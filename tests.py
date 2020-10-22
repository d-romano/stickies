from datetime import datetime, timedelta
import unittest

from config import Config
from app import create_app, db
from app.models import User, Note


class TestConfig(Config):
	''' Config flask testing variable and set db URI to memory '''
	TESTING=True
	SQLALCHEMY_DATABASE_URL='sqlite://'

class UserModelCase(unittest.TestCase):

	def setUp(self):
		''' Init test case flask app and db created. '''
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		''' When test ends remove data, drop tables and pop context. '''
		db.session.remove()
		db.drop_all()
		self.app_context.pop()


	def test_password_hash(self):
		''' Test password hash functionality. '''
		u1 = User(username='test', email='test@test.com')
		pw = 'test123'
		u1.setPassword(pw)

		db.session.add(u1)
		db.session.commit()

		self.assertFalse(u1.checkPassword('password'))
		self.assertTrue(u1.checkPassword(pw))
		

	def test_add_user(self):
		''' Verifying if users added to db. '''
		u1 = User(username='a', email='a@a.com')
		u2 = User(username='b', email='b@b.com')
		db.session.add_all([u1,u2])
		db.session.commit()
		self.assertFalse(User.query.filter_by(username='c').first())
		self.assertTrue(User.query.filter_by(username='a').first())
		self.assertFalse(User.query.filter_by(email='b@gmail.com').first())
		self.assertTrue(User.query.filter_by(email='b@b.com').first())


class NoteModelCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app(TestConfig)
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_notes(self):
		''' Testing note creation and deletion.'''
		u = User(username='a', email='a@a.com')
		db.session.add(u)
		db.session.commit()
		n = Note(title='test', body='test', userId = u.id)
		db.session.add(n)
		db.session.commit()
		self.assertTrue(Note.query.filter_by(title='test').first())
		self.assertFalse(Note.query.filter_by(id=2).first())
		# Remove post and attempt query
		db.session.delete(n)
		self.assertFalse(Note.query.filter_by(title='test').first())


if __name__ == '__main__':
	unittest.main(verbosity=2)