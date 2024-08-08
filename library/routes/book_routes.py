from flask import redirect, url_for, request, render_template, Blueprint
from library.extensions import db
from library.models import Book, Author, Publisher, AuthorPublisher
from library.forms import AddForm, UpdateForm, LimitForm
from library.maintenance import vacuum
from sqlalchemy import func

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
                msg='Author not found. Check your spelling.'
                return render_template('books/add_title.html', form=form, total=total, total_auth=total_auth, msg=msg)
                
        author_obj = Author.query.filter_by(fullname=author).first()
        rating = request.form['rating']
        rating = 0 if rating == '' else rating
        first_publish = form.first_publish.data
        pages = request.form['pages']
        pages = None if pages == '' else pages
        genre = request.form['genre']
        isbn10 = form.isbn10.data
        isbn13 = form.isbn13.data
        book_publisher = request.form['publisher']
        if book_publisher != '' and book_publisher != None and book_publisher != 'Null':
            if db.session.query(Publisher).filter_by(publ_name=book_publisher).first():
                book_publ=db.session.query(Publisher).filter_by(publ_name=book_publisher).first()
                publisher_id = book_publ.id
                if author_obj not in book_publ.authors:
                    book_publ.authors.append(author_obj)
            else:
                publisher_id = None
        else:
            publisher_id = None
        summary = request.form['summary']
        provisional_author = db.session.query(Author).filter_by(fullname=request.form['plusauthor']).first()        
        if not Book.query.filter_by(title=title, author=author, isbn10=isbn10, isbn13=isbn13).first():
            if provisional_author and publisher_id != None:
                co_author = provisional_author.fullname
                new_book = Book(title=title, author=author, co_author=co_author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, publisher_id=publisher_id, rating=rating, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
                if provisional_author not in book_publ.authors:
                    book_publ.authors.append(provisional_author)
            elif not provisional_author and publisher_id == None:
                new_book = Book(title=title, author=author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, rating=rating, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
            elif not provisional_author and publisher_id != None:
                new_book = Book(title=title, author=author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, rating=rating, publisher_id=publisher_id, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
            elif provisional_author and publisher_id == None:
                co_author = provisional_author.fullname
                new_book = Book(title=title, author=author, co_author=co_author, first_publish=first_publish, isbn10=isbn10, isbn13=isbn13, rating=rating, pages=pages, genre=genre, summary=summary, authors=[author_obj])
                db.session.add(new_book)
                if provisional_author not in book_publ.authors:
                    book_publ.authors.append(provisional_author)
            
            if provisional_author:
                if provisional_author not in new_book.authors:
                    new_book.authors.append(provisional_author)
                form.plusauthor.data = ''
            else:
                form.plusauthor.data = ''
            db.session.commit()
            
            # DB VACUUM
            vacuum()
            
            return redirect(url_for('author.bibliography', author=author))
            # return redirect(url_for('main.home', flag='authors_list'))
        else:
            msg = 'Book is already in the database'
            return render_template('books/add_title.html', form=form, total=total, total_auth=total_auth, msg=msg)
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
            if not pname:
                pname = None
                msg='Author not found. Check your spelling'
                return render_template('books/edit_title.html', form=form, book=book, total=total, total_auth=total_auth, msg=msg)
            if book.author in pname.penname:
                book.author = pname.fullname
                
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
        book_publisher = request.form['publisher']
        if book_publisher != '' and book_publisher != None and book_publisher != 'None':
            if db.session.query(Publisher).filter_by(publ_name=book_publisher).first():
                book_publ=db.session.query(Publisher).filter_by(publ_name=book_publisher).first()
                book.publisher_id = book_publ.id
                book_author = db.session.query(Author).filter_by(fullname=book.author).first()
                if provisional_author:
                    if provisional_author not in book_publ.authors:
                        book_publ.authors.append(provisional_author)
                if book_author not in book_publ.authors:
                    book_publ.authors.append(book_author)
            else:
                msg='Publisher not found. Check your spelling.'
                return render_template('books/edit_title.html', form=form, book=book, total=total, total_auth=total_auth, msg=msg)
        else:
            book.publisher_id = None
        book.first_publish = request.form['first_publish']
        if request.form['rating'] == '' or request.form['rating'] == None:
            book.rating = 0
        else:
            book.rating = request.form['rating']
        book.summary = request.form['summary']
        db.session.commit()
        
        # DB VACUUM
        vacuum()
        
        return redirect(url_for('author.bibliography', author=book.author))
        # return redirect(url_for('main.home', flag='authors_list'))

    return render_template('books/edit_title.html', form=form, book=book, total=total, total_auth=total_auth)

@book_bp.route('/delete_title/<int:id>', methods=['GET', 'POST'])
def delete_title(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    
    # DB VACUUM
    vacuum()
    
    return redirect(url_for('main.home', flag='books_list'))

@book_bp.route('/book_details/<int:id>')
def book_details(id):
    book = Book.query.get(id)
    if book.publisher_id != None and book.publisher_id != '' and book.publisher_id != 'Null':
        publisher = db.session.query(Publisher).get(book.publisher_id)
        publname = publisher.publ_name
        if publisher.publ_parent != None:
            publparent = publisher.publ_parent
    else:
        publname = None
        publparent = None
    return render_template('books/book_details.html', book=book, publparent=publparent, publname=publname)

@book_bp.route('/books_by_leter', methods=['GET', 'POST'])
def books_by_letter():
    form=LimitForm()
    letter=request.args.get('letter')
    authors = db.session.query(Author).all()
    total_auth = len(authors)
    books = db.session.query(Book).all()
    total = len(books)
    total_publishers = len(db.session.query(Publisher).all())
    lim=form.limit.data
    if lim != None and lim != 'None' and lim != '' and lim != '0':
        if letter != '*':
            books_by_letter = db.session.query(Book).filter(Book.title.istartswith(letter)).order_by(func.lower(Book.title), func.lower(Book.author)).limit(lim).all()
        else:
            books_by_letter = db.session.query(Book).order_by(func.lower(Book.title), func.lower(Book.author)).limit(lim).all()
    else:
        if letter != '*':
            books_by_letter = db.session.query(Book).filter(Book.title.istartswith(letter)).order_by(func.lower(Book.title), func.lower(Book.author)).all()
        else:
            books_by_letter = db.session.query(Book).order_by(func.lower(Book.title), func.lower(Book.author)).all()
            
    authors_to_count=[book.author for book in books_by_letter]       
    for book in books_by_letter:
        for author in book.authors:
            authors_to_count.append(author.fullname) if author.fullname not in authors_to_count else exit
    authors_count = len(set(authors_to_count))
    
    return render_template('index.html', flag='books_by_letter', books_by_letter=books_by_letter, authors=authors, total=total, total_auth=total_auth, total_publishers=total_publishers, letter=letter, form=form, authors_count=authors_count)
