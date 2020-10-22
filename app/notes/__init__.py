from app.auth import login_required
from app.models import User, Note
from app import db
from app.notes.forms import NoteForm
from datetime import datetime
from flask import Blueprint, url_for, redirect, render_template, session, g, request, flash, abort
from functools import wraps

bp = Blueprint('main', __name__)


def validate_user(view):
	@wraps(view)
	def check_wrapper(*args, **kwargs):
		''' Validates that note exists and that user is owner '''
		id = kwargs['id']

		note = Note.query.filter_by(id=id).first_or_404()
		kwargs['note'] = note
		if note.userId == g.user.id:
			return view(*args, **kwargs)
		else:
			abort(403)
	return check_wrapper

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
	''' Index page on website. Displays login or user posts '''
	username = ""
	notes = None
	if g.user:
		page = request.args.get('page', 1, type=int)
		username = g.user.username
		notes = Note.query.filter_by(userId = g.user.id).order_by(Note.created.desc()).paginate(page,
			5, False)
		next_url = url_for('main.index', page=notes.next_num) if notes.has_next else None
		prev_url = url_for('main.index', page=notes.prev_num) if notes.has_prev else None

	return render_template('notes/index.html', title='index', username=username, notes=notes.items, next_url=next_url, prev_url=prev_url)

@bp.route('/newnote', methods=['GET', 'POST'])
@login_required
def new_note():
	''' Allows logged-in user to create and save a new note.'''
	form = NoteForm()
	if request.method=='POST' and form.validate():
		note = Note.create(title = form.title.data, body = orm.body.data, user = g.user)
		flash("Note created.")
		return redirect(url_for('main.view', id=note.id))

	return render_template('notes/newnote.html', title = "New Note", form = form)


@bp.route('/view/<int:id>', methods=['GET'])
@login_required
@validate_user
def view(id, note):
	''' View a note and its details. '''
	# Validate note exists and belongs to user
	return render_template('notes/view.html', title = note.title, note = note)


@bp.route('/update/<int:id>', methods=['GET','POST'])
@login_required
@validate_user
def update(id, note):
	''' update note ID'''
	#note = Note.query.filter_by(id=id).first_or_404()
	
	form = NoteForm()


	if request.method=='POST' and form.validate():
		note.title = form.title.data
		note.body = form.body.data
		note.modified = datetime.utcnow()
		db.session.commit()
		flash("Note updated successfully!")
		return redirect(url_for('main.view', id = note.id))
	elif request.method =='GET':
		form.title.data = note.title
		form.body.data = note.body


	return render_template('notes/newnote.html', title = 'Update', form = form)

@bp.route('/delete/<int:id>', methods=['GET'])
@login_required
@validate_user
def deletePost(id, note):
	# Check if note exists before attempting delete.
	if note and note.userId == g.user.id:
		db.session.delete(note)
		db.session.commit()
		flash("Note deleted successfully.")


	return redirect(url_for('main.index'))