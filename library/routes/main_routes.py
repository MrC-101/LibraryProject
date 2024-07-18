from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import AddForm, SearchForm, UpdateForm


main_bp = Blueprint('main',__name__)

@main_bp.route('/init')
def init():
    # db.create_all()

    # new_auth=Author(fullname='Isaac Asimov', email='iasimov@gmail.com')
    # db.session.add(new_auth)
    # db.session.commit()

    # author = Author.query.filter_by(fullname='Elena Alpha').first()
    # print(author)

    # book=Book(title="The 10th Commandment", author='Elena Alpha', first_publish=2005, isbn='123456780X', rating=9.9, authors=[author])
    # db.session.add(book)

    # author.books.append(book)

    # db.session.commit()
    
    # elena = db.session.query(Author).filter_by(fullname='Elena Alpha').first()
    # books = [book.title for book in elena.books]
    # print(f"Elena's Books: {', '.join(books)}")
    
    return redirect(url_for('main.home'))
    # book = Book.query.get(46)
    # print(book)
    # author=Author.query.get(1)
    # print(author)
    # new_auth=Author(fullname='Elena Alpha', email='elena.a@gmail.com')
    # db.session.add(new_auth)
    # db.session.commit()
    
    # book = Book.query.get('2')
    # print(book)
    # print(book.author_lname)
    # print(book.authors.author.id)
    
@main_bp.route('/')
def home():
    books = Book.query.order_by('author').order_by('first_publish').order_by('title').all()
    authors = Author.query.all()
    total_auth = len(authors)
    total = len(books)
    return render_template('index.html', books=books, total_auth=total_auth, total=total)


@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    books = Book.query.order_by('author').order_by('title').all()
    authors = Author.query.all()
    total_auth = len(authors)
    total = len(books)
    form = SearchForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            books = Book.query.order_by('author').order_by('title').all()
            total = len(books)
            title_returned = form.title.data
            author_returned = form.author.data
            isbn_returned = form.isbn.data
            form.title.data = ''
            form.author.data = ''
            if Book.query.filter_by(title=title_returned, author=author_returned).first():
                book = Book.query.filter_by(title=title_returned).filter_by(author=author_returned).first()
                return redirect(url_for('book.edit_title', id=book.id, total=total, total_auth=total_auth))
            elif Book.query.filter_by(title=title_returned).first() and not Book.query.filter_by(
                    author=author_returned).first():
                books = Book.query.filter_by(title=title_returned).all()
                if len(books) > 1:
                    form = SearchForm()
                    return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
                else:
                    book = Book.query.filter_by(title=title_returned).first()
                    return redirect(url_for('author.bibliography', author=book.author, id=book.id, total=total, total_auth=total_auth))
            elif Book.query.filter_by(author=author_returned).first() and not Book.query.filter_by(title=title_returned).first():
                books = Book.query.filter_by(author=author_returned).all()
                if len(books) > 1:
                    form = SearchForm()
                    print(author_returned)
                    return redirect(url_for('author.bibliography', author=author_returned, form=form, books=books, total=total, total_auth=total_auth))
                elif len(books) == 1:
                    book = Book.query.filter_by(author=author_returned).first()
                    return redirect(url_for('author.bibliography', author=author_returned, id=book.id, total=total, total_auth=total_auth))
            elif Book.query.filter_by(isbn=isbn_returned):
                book = Book.query.filter_by(isbn=isbn_returned).first()
                return redirect(url_for('author.bibliography', author=book.author, total=total, total_auth=total_auth))

            else:
                flash('Book not found')
                books = Book.query.order_by('author').all()
                form = SearchForm()
                return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
    # id = request.args.get('id')
    # book = Book.query.get(id)
    return render_template('search.html', form=form, books=books, total_auth=total_auth, total=total)
