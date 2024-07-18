from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import AddForm, SearchForm, UpdateForm

author_bp = Blueprint('author',__name__)

@author_bp.route('/bibliography', methods=['GET', 'POST'])
def bibliography():
    books = Book.query.order_by('author').order_by('first_publish').order_by('title').all()
    total = len(books)
    authors = Author.query.all()
    total_auth = len(authors)
    
    author = request.args.get('author')
    books = Book.query.filter_by(author=author).order_by('first_publish').order_by('title').all()
    author_total = len(books)
    return render_template('authors/bibliography.html', books=books, author=author, total=total, author_total=author_total, total_auth=total_auth)