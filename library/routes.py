from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import AddForm, SearchForm, UpdateForm


main_bp = Blueprint('main',__name__)

@main_bp.route('/init')
def init():
    # db.create_all()
    new_auth=Author(fullname='Isaac Asimov', email='iasimov@gmail.com')
    db.session.add(new_auth)
    db.session.commit()
    # author = db.session.execute(db.select(Author).order_by(Author.fullname)).scalar()
    # print(author)
    # book=Book(title="First Kiss", author='Elena Alpha', first_publish=1995, isbn='123450789X', rating=9.9, authors=[author])
    # db.session.add(book)
    # author.books.append(book)
    db.session.commit()
    
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
    total = len(books)
    return render_template('index.html', books=books, total=total)

@main_bp.route('/add_title', methods=['GET', 'POST'])
def add_title():
    books = Book.query.order_by('author').order_by('title').all()
    total = len(books)
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
        return render_template('add_title.html', form=form, total=total)

@main_bp.route('/edit_rating', methods=['GET', 'POST'])
def edit_rating():
    books = Book.query.order_by('author').order_by('title').all()
    total = len(books)
    id = request.args.get('id')
    book = Book.query.get(id)
    if request.method == 'POST':
        book.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('edit_rating.html', book=book, total=total)


@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    books = Book.query.order_by('author').order_by('title').all()
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
                return redirect(url_for('main.edit_title', id=book.id, total=total))
            elif Book.query.filter_by(title=title_returned).first() and not Book.query.filter_by(
                    author=author_returned).first():
                books = Book.query.filter_by(title=title_returned).all()
                if len(books) > 1:
                    form = SearchForm()
                    return render_template('search.html', form=form, books=books, total=total)
                else:
                    book = Book.query.filter_by(title=title_returned).first()
                    return redirect(url_for('main.bibliography', author=book.author, id=book.id, total=total))
            elif Book.query.filter_by(author=author_returned).first() and not Book.query.filter_by(title=title_returned).first():
                books = Book.query.filter_by(author=author_returned).all()
                if len(books) > 1:
                    form = SearchForm()
                    print(author_returned)
                    return redirect(url_for('main.bibliography', author=author_returned, form=form, books=books, total=total))
                elif len(books) == 1:
                    book = Book.query.filter_by(author=author_returned).first()
                    return redirect(url_for('main.bibliography', author=author_returned, id=book.id, total=total))
            elif Book.query.filter_by(isbn=isbn_returned):
                book = Book.query.filter_by(isbn=isbn_returned).first()
                return redirect(url_for('main.bibliography', author=book.author, total=total))

            else:
                flash('Book not found')
                books = Book.query.order_by('author').all()
                form = SearchForm()
                return render_template('search.html', form=form, books=books, total=total)
    id = request.args.get('id')
    book = Book.query.get(id)
    return render_template('search.html', form=form, books=books, total=total)

@main_bp.route('/edit_title', methods=['GET', 'POST'])
def edit_title():
    books = Book.query.order_by('author').order_by('title').all()
    total = len(books)
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

    return render_template('edit_title.html', form=form, book=book, total=total)

@main_bp.route('/delete_title/<int:id>', methods=['GET', 'POST'])
def delete_title(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route('/book_details/<int:id>')
def book_details(id):
    books = Book.query.order_by('author').order_by('title').all()
    total = len(books)
    book = Book.query.get(id)
    return render_template('book_details.html', book=book, total=total)

@main_bp.route('/bibliography', methods=['GET', 'POST'])
def bibliography():
    books = Book.query.order_by('author').order_by('first_publish').order_by('title').all()
    total = len(books)
    author = request.args.get('author')
    books = Book.query.filter_by(author=author).order_by('first_publish').order_by('title').all()
    author_total = len(books)
    return render_template('bibliography.html', books=books, author=author, total=total, author_total=author_total)