from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class CommentForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])


class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = CKEditorField('Text', validators=[DataRequired()])
    tags = SelectMultipleField('Choose a tag')
