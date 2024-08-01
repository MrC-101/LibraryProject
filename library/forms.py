from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Optional
from wtforms_alchemy import QuerySelectMultipleField

class SearchForm(FlaskForm):
    title = StringField(label='title', validators=[Optional()])
    author = StringField(label='author', validators=[Optional()])
    isbn10 = StringField(label='isbn10', validators=[Optional()])
    isbn13 = StringField(label='isbn13', validators=[Optional()])
    submit = SubmitField(label='Search')

class SearchBooksForm(FlaskForm):
    title = StringField(label='title', validators=[Optional()])
    submit = SubmitField(label='Search')
    
class SearchAuthorsForm(FlaskForm):
    author = StringField(label='author', validators=[Optional()])
    submit = SubmitField(label='Search')

class SearchAllItemsForm(FlaskForm):
    all_items = StringField(label='all_items', validators=[Optional()])
    submit = SubmitField(label='Search')
      
class UpdateForm(FlaskForm):
    coauths = QuerySelectMultipleField('Coauths')
    title = StringField(label='title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    co_author = StringField(label='co_author')
    plusauthor = StringField(label='+author')
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    pages = IntegerField(label='pages', validators=[Optional()])
    genre = StringField(label='genre')
    isbn10 = StringField(label='isbn10')
    isbn13 = StringField(label='isbn13')
    publisher = StringField(label='publisher')
    rating = FloatField(label='rating', validators=[Optional()])
    summary = TextAreaField(label='summary', validators=[Optional()])
    submit = SubmitField(label='Update')

class AddForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    author = StringField(label='author', validators=[DataRequired()])
    plusauthor = StringField(label='+author')
    first_publish = IntegerField(label='first_publish', validators=[DataRequired()])
    pages = IntegerField(label='pages', validators=[Optional()])
    genre = StringField(label='genre')
    isbn10 = StringField(label='isbn10')
    isbn13 = StringField(label='isbn13')
    publisher = StringField(label='publisher')
    rating = FloatField(label='rating', validators=[Optional()])
    summary = TextAreaField(label='summary', validators=[Optional()])
    submit = SubmitField(label='Add Title')

class AddAuthorForm(FlaskForm):
    penname = StringField(label='Pen Name')
    name_pref = StringField(label='Name Prefix')
    fname = StringField(label='First Name')
    midname = StringField(label='Middle Name')
    lname = StringField(label='Last Name', validators=[DataRequired()])
    name_suf = StringField(label='Name Suffix')
    penname = StringField(label='Pen Name')
    gender = SelectField(label='Gender', choices=[(1,'Male'),(2,'Female')])
    country = StringField(label='Country')
    city = StringField(label='City')
    born = StringField(label='Born In', validators=[Optional()])
    died = StringField(label='Died', validators=[Optional()])
    email = StringField(label='email')
    bio = TextAreaField(label='Bio', validators=[Optional()])
    submit = SubmitField(label='Add Author')
    
class EditAuthorForm(FlaskForm):
    penname = StringField(label='Pen Name')
    name_pref = StringField(label='Name Prefix')
    fname = StringField(label='First Name')
    midname = StringField(label='Middle Name')
    lname = StringField(label='Last Name', validators=[DataRequired()])
    name_suf = StringField(label='Name Suffix')
    gender = SelectField(label='Gender', choices=[('Male','Male'),('Female','Female')])
    country = StringField(label='country')
    city = StringField(label='City')
    born = StringField(label='born')
    died = StringField(label='died')
    email = StringField(label='email')
    bio = TextAreaField(label='bio')
    submit = SubmitField(label='Update')
        
class AddPublisherForm(FlaskForm):
    publname = StringField(label='Name', validators=[DataRequired()])
    publfounder = StringField(label='Founder')
    publparent = StringField(label='Parent')
    publest = StringField(label='Est')
    publcountry = StringField(label='Country')
    publcity = StringField(label='City')
    publaddress = StringField(label='Address')
    publemail = StringField(label='Email')
    publwebsite= StringField(label='Website')
    submit = SubmitField(label='Add Publisher')    
    
class EditPublisherForm(FlaskForm):
    publname = StringField(label='Name', validators=[DataRequired()])
    publfounder = StringField(label='Founder')
    publparent = StringField(label='Parent')
    publest = StringField(label='Est')
    publcountry = StringField(label='Country')
    publcity = StringField(label='City')
    publaddress = StringField(label='Address')
    publemail = StringField(label='Email')
    publwebsite= StringField(label='Website')
    submit = SubmitField(label='Update')  