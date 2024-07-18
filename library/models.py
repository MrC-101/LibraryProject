
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
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=True)
    first_publish = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    authors = db.relationship('Author', secondary='book_author', back_populates='books')
    
    @property
    def author_fname(self):
        fname = self.author.split()[0]
        return fname
    
    @property
    def author_lname(self):
        lname = self.author.split()[1]
        return lname
    
    def __repr__(self):
        return f'DB_ID: {self.id},  Title: {self.title},  Author: {self.author}, Authors: {self.authors}'
    
class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False) 
    books = db.relationship("Book", secondary='book_author', back_populates='authors')
    
    @property
    def fname(self):
        fname = self.fullname.split()[0]
        return fname
    
    @property
    def lname(self):
        lname = self.fullname.split()[1]
        return lname
        
    def __repr__(self):
        return f'DB_ID: {self.id},  Name: {self.fname} {self.lname}, {self.books}'

