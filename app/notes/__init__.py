from app.auth import login_required
from app.models import User, Note
from app import db
from app.notes.forms import NoteForm

from flask import Blueprint, url_for, redirect, render_template, session, g, request, flash, abort


bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
	''' Index page on website. Displays login or user posts '''
	username = ""
	notes = None
	if g.user:
		username = g.user.username
		notes = Note.query.filter_by(userId=g.user.id).all()
	return render_template('notes/index.html', title='index', username=username, notes=notes)

@bp.route('/newnote', methods=['GET', 'POST'])
@login_required
def new_note():
	''' Allows logged-in user to create and save a new note.'''
	form = NoteForm()
	if request.method=='POST' and form.validate():
		note = Note.create(title=form.title.data, body=form.body.data, user=g.user)
		flash("Note created.")
		return redirect(url_for('main.view', id=note.id))

	return render_template('notes/newnote.html', title="New Note", form=form)

@bp.route('/view/<int:id>', methods=['GET','POST'])
@login_required
def view(id):
	''' View note ID'''
	note = Note.query.filter_by(id=id).first_or_404()
	if id == 5:
		print(note.id)
	if note and note.userId == g.user.id:
		return "{}".format(note.userId)
	else:
		return 'Nothing here :('

@bp.route('/delete/<int:id>', methods=['GET'])
@login_required
def deletePost(id):
	''' Allows deletion of a post if owned by current user and exists, '''
	note = Note.query.filter_by(id=id).first_or_404()

	# Check if note exists before attempting delete.
	if note and note.userId == g.user.id:
		db.session.delete(note)
		db.session.commit()
		flash("Note deleted successfully.")
	else:
		flash("You do not have permission to do that.")
		abort(403)

	return redirect(url_for('main.index'))