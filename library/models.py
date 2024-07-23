
# from sqlalchemy.orm import relationship
# from sqlalchemy import Table
from library.extensions import db

# book_author = db.Table('book_author',
#                     db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True),
#                     db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
#                     )
class BookAuthor(db.Model):
    __tablename__ = "book_author"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    co_author = db.Column(db.String, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    isbn10 = db.Column(db.String, nullable=True)
    isbn13 = db.Column(db.String, nullable=True)
    first_publish = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String, nullable=True)
    summary = db.Column(db.Text, default='', nullable=True)
    authors = db.relationship('Author', secondary='book_author', back_populates='books')
    
    def __repr__(self):
        return f'DB_ID: {self.id},  Title: {self.title},  Author: {self.author} Published: {self.first_publish}'
    
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    penname = db.Column(db.String, nullable=True)
    fname = db.Column(db.String, nullable=True)
    lname = db.Column(db.String, nullable=True)
    midname = db.Column(db.String, nullable=True)
    name_pref = db.Column(db.String, nullable=True)
    name_suf = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=True)
    fullname = db.Column(db.String, nullable=False)
    country = db.Column(db.String, default='', nullable=True)
    city = db.Column(db.String, default='', nullable = True)
    born = db.Column(db.String(4), default='', nullable=True)
    died = db.Column(db.String(4), default='', nullable=True)
    bio = db.Column(db.Text, default='', nullable=True)
    email = db.Column(db.String, default='', nullable=True)
    books = db.relationship("Book", secondary='book_author', back_populates='authors')
    
    def __repr__(self):
            return f'DB_ID: {self.id},  Name: {self.fullname}, {self.books}'
