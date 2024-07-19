from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import AddForm, UpdateForm

book_bp = Blueprint('book',__name__)

@book_bp.route('/add_title', methods=['GET', 'POST'])
def add_title():
    books = db.session.query(Book).all()
    total = len(books)
    authors = Author.query.all()
    total_auth = len(authors)
    form = AddForm()
    if form.validate_on_submit():
        title = request.form['title']
        author = request.form['author']
        author_obj = Author.query.filter_by(fullname=author).first()
        rating = request.form['rating']
        first_publish = form.first_publish.data
        isbn = form.isbn.data
        if not Book.query.filter_by(title=title, author=author, isbn=isbn).first():
            new_book = Book(title=title, author=author, first_publish=first_publish, isbn=isbn, rating=rating, authors=[author_obj])
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('That book is already in the library.')
    else:
        return render_template('books/add_title.html', form=form, total=total, total_auth=total_auth)

@book_bp.route('/edit_title', methods=['GET', 'POST'])
def edit_title():
    books = db.session.query(Book).all()
    total = len(books)
    authors = Author.query.all()
    total_auth = len(authors)
    form = UpdateForm()
    id = request.args.get('id')
    book = Book.query.get(id)
    if form.validate_on_submit():
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.first_publish = request.form['first_publish']
        book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('books/edit_title.html', form=form, book=book, total=total, total_auth=total_auth)

@book_bp.route('/delete_title/<int:id>', methods=['GET', 'POST'])
def delete_title(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.home'))

@book_bp.route('/book_details/<int:id>')
def book_details(id):
    books = db.session.query(Book).all()
    total = len(books)
    authors = Author.query.all()
    total_auth = len(authors)
    book = Book.query.get(id)
    return render_template('books/book_details.html', book=book, total=total, total_auth=total_auth)

# @book_bp.route('/edit_rating', methods=['GET', 'POST'])
# def edit_rating():
#     books = Book.query.order_by('author').order_by('title').all()
#     total = len(books)
#     authors = Author.query.all()
#     total_auth = len(authors)
#     id = request.args.get('id')
#     book = Book.query.get(id)
#     if request.method == 'POST':
#         book.rating = request.form['rating']
#         db.session.commit()
#         return redirect(url_for('main.home'))

#     return render_template('books/edit_rating.html', book=book, total=total, total_auth=total_auth)