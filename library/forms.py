from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Optional


class SearchForm(FlaskForm):
    title = StringField(label='title', validators=[Optional()])
    author = StringField(label='author', validators=[Optional()])
    isbn = StringField(label='isbn', validators=[Optional()])
    submit = SubmitField(label='Search')
    
class UpdateForm(FlaskForm):
    title = StringField(label='title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    plusauthor = StringField(label='+author')
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    isbn = StringField(label='isbn')
    rating = FloatField(label='rating')
    submit = SubmitField(label='Update')

class AddForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    plusauthor = StringField(label='+author')
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    isbn = StringField(label='isbn')
    rating = FloatField(label='rating')
    submit = SubmitField(label='Add Title')

class AddAuthorForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    country = StringField(label='Country')
    city = StringField(label='City')
    born = StringField(label='Born In', validators=[Optional()])
    died = StringField(label='Died', validators=[Optional()])
    email = StringField(label='email')
    bio = TextAreaField(label='Bio', validators=[Optional()])
    submit = SubmitField(label='Add Author')
    
class EditAuthorForm(FlaskForm):
    name = StringField(label='name', validators=[DataRequired()])
    country = StringField(label='country')
    city = StringField(label='City')
    born = StringField(label='born')
    died = StringField(label='died')
    email = StringField(label='email')
    bio = TextAreaField(label='bio')
    submit = SubmitField(label='Update')
        
    