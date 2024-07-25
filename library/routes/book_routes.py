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
        if not db.session.query(Author).filter_by(fullname=author).first():
            pname = db.session.query(Author).filter(Author.penname.icontains(author)).first()
            # pname = db.session.query(Author).filter_by(penname=author).first()
            if pname:
                if author in pname.penname:
                    author = pname.fullname
            else:
                flash('Author not found. Check Author Name.')
                return render_template('books/add_title.html', form=form, total=total, total_auth=total_auth)
                
        author_obj = Author.query.filter_by(fullname=author).first()
        rating = request.form['rating']
        rating = 0 if rating == '' else rating
        first_publish = form.first_publish.data
        pages = request.form['pages']
        pages = None if pages == '' else pages
        genre = request.form['genre']
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        summary = request.form['summary']
        provisional_author = db.session.query(Author).filter_by(fullname=request.form['plusauthor']).first()        
        if not Book.query.filter_by(title=title, author=author, isbn10=isbn10, isbn13=isbn13).first():
            if provisional_author:
                co_author = provisional_author.fullname
                new_book = Book(title=title, author=author, co_author=co_author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, rating=rating, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
            else:
                new_book = Book(title=title, author=author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, rating=rating, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
            if provisional_author:
                new_book.authors.append(provisional_author)
                form.plusauthor.data = ''
            else:
                form.plusauthor.data = ''
            db.session.commit()
            return redirect(url_for('author.bibliography', author=author))
            # return redirect(url_for('main.home', flag='authors_list'))
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
    id = request.args.get('id')
    book = Book.query.get(id)
    # form = UpdateForm(summary=book.summary, data={"coauths":book.authors})
    # we do not need coauths preselected because selected will be deleted
    form = UpdateForm(summary=book.summary)
    form.coauths.query = book.authors   
    if form.validate_on_submit():
        for author in form.coauths.data:
            book.authors.remove(author)
        book.title = request.form['title']
        book.author = request.form['author']
        if not db.session.query(Author).filter_by(fullname=book.author).first():
            pname = db.session.query(Author).filter(Author.penname.icontains(book.author)).first()
            # pname = db.session.query(Author).filter_by(penname=book.author).first()
            if book.author in pname.penname:
                book.author = pname.fullname
            else:
                flash('Author not found')
        provisional_author = db.session.query(Author).filter_by(fullname=request.form['plusauthor']).first()
        if provisional_author:
            book.authors.append(provisional_author)
            form.plusauthor.data = ''
        else:
            form.plusauthor.data = ''
        if request.form['pages'] == '':
            book.pages = None
        else:
            book.pages = request.form['pages']
        book.genre = request.form['genre']
        book.isbn10 = request.form['isbn10']
        book.isbn13 = request.form['isbn13']
        book.first_publish = request.form['first_publish']
        if request.form['rating'] == '' or request.form['rating'] == None:
            book.rating = 0
        else:
            book.rating = request.form['rating']
        book.summary = request.form['summary']
        db.session.commit()
        return redirect(url_for('author.bibliography', author=book.author))
        # return redirect(url_for('main.home', flag='authors_list'))

    return render_template('books/edit_title.html', form=form, book=book, total=total, total_auth=total_auth)

@book_bp.route('/delete_title/<int:id>', methods=['GET', 'POST'])
def delete_title(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.home'))

@book_bp.route('/book_details/<int:id>')
def book_details(id):
    book = Book.query.get(id)
    return render_template('books/book_details.html', book=book)

@book_bp.route('/books_by_leter')
def books_by_letter():
    letter=request.args.get('letter')
    authors = db.session.query(Author).all()
    total_auth = len(authors)
    books = db.session.query(Book).all()
    total = len(books)
    if letter != '*':
        books_by_letter = db.session.query(Book).filter(Book.title.istartswith(letter)).all()
    else:
        books_by_letter = db.session.query(Book).order_by('author', 'first_publish', 'title').all()
    return render_template('index.html', flag='books_by_letter', books_by_letter=books_by_letter, total=total, total_auth=total_auth)


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