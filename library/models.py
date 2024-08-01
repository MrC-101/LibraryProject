
# from sqlalchemy.orm import relationship
# from sqlalchemy import Table,Index, func, cast, text
from library.extensions import db


class BookAuthor(db.Model):
    __tablename__ = "book_author"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))


class AuthorPublisher(db.Model):
    __tablename__ = 'author_publisher'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"))

    
class Publisher(db.Model):
    __tablename__ = 'publishers'
    id = db.Column(db.Integer, primary_key=True)
    publ_name = db.Column(db.String, nullable=False)
    publ_founder = db.Column(db.String, nullable=True)
    publ_parent = db.Column(db.String, nullable=True)
    publ_est = db.Column(db.String, nullable=True)
    publ_country = db.Column(db.String, nullable=True)
    publ_city = db.Column(db.String, nullable = True)
    publ_address = db.Column(db.String, nullable=True)
    publ_email = db.Column(db.String, nullable=True)
    publ_website = db.Column(db.String, nullable=True)
    books = db.relationship('Book', back_populates='publisher')
    authors = db.relationship('Author', secondary='author_publisher', back_populates='publishers')
    
    def __repr__(self):
        return f'{self.publ_name}'

       
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    co_author = db.Column(db.String, nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    isbn10 = db.Column(db.String, nullable=True)
    isbn13 = db.Column(db.String, nullable=True)
    first_publish = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String, nullable=True)
    summary = db.Column(db.Text, default='', nullable=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"))
    publisher = db.relationship('Publisher', back_populates='books', uselist=False)
    authors = db.relationship('Author', secondary='book_author', back_populates='books')
    
    def __repr__(self):
        return f'ID: {self.id},  Title: {self.title},  Author: {self.author} Published: {self.first_publish}'

    
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
    publishers = db.relationship('Publisher', secondary='author_publisher', back_populates='authors')
    
    def __repr__(self):
            return f'{self.fullname} (id: {self.id})'
