from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email, ValidationError


class NoteForm(FlaskForm):
	title = StringField("Title", validators=[InputRequired(), Length(max=50)])
	body = TextAreaField("Body", validators=[Length(max=255)])
	submit = SubmitField("Save")