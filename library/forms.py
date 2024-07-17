from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, ValidationError, Optional


class SearchForm(FlaskForm):
    title = StringField(label='title', validators=[Optional()])
    author = StringField(label='author', validators=[Optional()])
    isbn = StringField(label='isbn', validators=[Optional()])
    submit = SubmitField(label='Search')
    
class UpdateForm(FlaskForm):
    title = StringField(label='title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    isbn = StringField(label='isbn')
    rating = FloatField(label='rating')
    submit = SubmitField(label='Update')

class AddForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    isbn = StringField(label='isbn')
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    rating = FloatField(label='rating', validators=[Optional()])
    submit = SubmitField(label='Add Title')