from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import SearchForm
import operator

main_bp = Blueprint('main',__name__)

@main_bp.route('/init')
def init():
    
    book = db.session.query(Book).get(256)
    # for i in range(len(book.authors)):
    #     print(book.authors[i].fullname)
    
    # book.co_author=''
    # db.session.commit()
    
    # author=db.session.query(Author).get(60)
    # print(author.fullname)
    # print('auth books: ', len(author.books))
    # print('b1 auths: ', len(author.books[0].authors))
    # print('b2 auths: ', len(author.books[1].authors))
    # print('b3 auths: ', len(author.books[2].authors))
    # books = db.session.query(Book).filter_by(title='First Kiss').all()
    # for book in books:
    #     for author in book.authors:
    #         print(author.fullname, book.title, book.id)
                
    # for author in book.authors:
    #     print(author.fullname)
        
    # for author in book.authors:
    #     print(author.fullname, book.title, book.id)
            
    # MrC = db.session.query(Author).filter_by(fullname='MrC').first()
    # book = db.session.query(Book).filter_by(id=7).first()
    # book.authors.append(MrC)
    # db.session.commit()
    # author = db.session.query(Author).get(51)
    # print(author.books)
    # author = db.session.query(Author).get(1)
    # print(author.books)
    # books = db.session.query(Book).filter_by(title='First Kiss').all()
    # for book in books:
    #    for author in book.authors:
    #        print(book.title, book.id, author.fullname)
    # db.create_all()
    # authors=[
    #       Author(fullname='Gabriel García Márquez'),
    #       Author(fullname='Umberto Eco'),
    #       Author(fullname='William Faulkner'),
    #       Author(fullname='Aesop'),
    #       Author(fullname='Fyodor Dostoevsky'),
    #       Author(fullname='Dante Alighieri'),
    #       Author(fullname='Lev Tolstoy'),
    #       Author(fullname='Victor Hugo'),
    #       Author(fullname='William Shakespeare'),
    #       Author(fullname='Johann Wolfgang von Goethe'),
    #       Author(fullname='Miguel de Cervantes y Saavedra'),
    #       Author(fullname='Italo Calvino'),
    #       Author(fullname='Stendhal'),
    #       Author(fullname='Charles Baudelaire'),
    #       Author(fullname='Marcel Proust'),
    #       Author(fullname='Giovanni Boccaccio'),
    #       Author(fullname='Alexander Pushkin'),
    #       Author(fullname='Jalaluddin Muhammad Rumi'),
    #       Author(fullname='Franz Kafka'),
    #       Author(fullname='Anton Chekhov'),
    #       Author(fullname='Angie Thomas'),
    #       Author(fullname='Colleen Hoover'),
    #       Author(fullname='Neil Gaiman'),
    #       Author(fullname='Dan Brown'),
    #       Author(fullname='Colson Whitehead'),
    #       Author(fullname='Ocean Vuong'),
    #       Author(fullname='Taylor Jenkins Reid'),
    #       Author(fullname='Silvia Moreno-Garcia'),
    #       Author(fullname='Brit Bennett'),
    #       Author(fullname='Leigh Bardugo'),
    #       Author(fullname='Sarah J. Maas'),
    #       Author(fullname='Kazuo Ishiguro'),
    #       Author(fullname='Veronica Roth'),
    #       Author(fullname='Stephen King'),
    #       Author(fullname='John Green')
    # ]
    
    # for author in authors:
    #     db.session.add(author)
    #     db.session.commit()

    # a=Author(fullname='Eoin Colfer')
    # db.session.add(a)
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
    books_totals = db.session.query(Book).order_by('author', 'first_publish', 'title').all()
    authors_totals = Author.query.all()
    total_auth = len(authors_totals)
    total = len(books_totals)
    flag = request.args.get('flag')
    authors = db.session.query(Author).order_by('fullname').all()
    # # books=[]
    # # for author in authors:
    # #     for book in author.books:
    # #         books.append(book)
    # books=[book for author in authors for book in author.books]
    # books.sort(key=operator.attrgetter('author', 'first_publish', 'title'))
    books = db.session.query(Book).order_by('author', 'first_publish', 'title').all()
    if flag == 'authors_list':
        return render_template('index.html', books=books, authors=authors, flag=flag, total=total, total_auth=total_auth)
    else: 
        return render_template('index.html', books=books, title='', total=total, total_auth=total_auth)

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    books = db.session.query(Book).all()
    authors = Author.query.all()
    total_auth = len(authors)
    total = len(books)
    form = SearchForm()
    flag = request.args.get('flag')
    if request.method == 'POST':
        if form.validate_on_submit():
            books = db.session.query(Book).all()
            total = len(books)
            title_returned = form.title.data
            author_returned = form.author.data
            isbn_returned = form.isbn.data
            form.title.data = ''
            form.author.data = ''
            form.isbn.data = ''
            
            if Book.query.filter_by(title=title_returned, author=author_returned).first():
                book = Book.query.filter_by(title=title_returned).filter_by(author=author_returned).first()
                return redirect(url_for('book.edit_title', id=book.id, total=total, total_auth=total_auth))
            
            elif Book.query.filter_by(title=title_returned).first() and not Book.query.filter_by(author=author_returned).first():
                books = Book.query.filter_by(title=title_returned).all()
                if len(books) > 1:
                    form = SearchForm()
                    return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
                else:
                    book = Book.query.filter_by(title=title_returned).first()
                    return redirect(url_for('book.edit_title', author=book.author, id=book.id, total=total, total_auth=total_auth))
            
            elif Book.query.filter_by(author=author_returned).first() and not Book.query.filter_by(title=title_returned).first() or Author.query.filter_by(fullname=author_returned).first():
                author_obj = Author.query.filter_by(fullname=author_returned).first()
                books = Book.query.filter_by(author=author_returned).all()
          
                if len(books) > 1:
                    form = SearchForm()
                    for _ in range(10):
                        print('here here 1')
                    return redirect(url_for('author.bibliography', author=author_returned, author_id=author_obj.id, form=form, books=books, total=total, total_auth=total_auth))
                
                elif len(books) == 1:
                    book = Book.query.filter_by(author=author_returned).first()
                    return redirect(url_for('book.edit_title', author=author_returned, author_id=author_obj.id, id=book.id, total=total, total_auth=total_auth))
                
                else:
                    return redirect(url_for('author.edit_author', author=author_returned, id=author_obj.id))
            
            elif Book.query.filter_by(isbn=isbn_returned) and isbn_returned is not '':
                book = Book.query.filter_by(isbn=isbn_returned).first()
                return redirect(url_for('author.bibliography', author=book.author))
            
            else:
                flash('Nothing found in the Database')
                books = Book.query.order_by('author').all()
                form = SearchForm()
                return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
    else:
        return render_template('search.html', form=form, books=books, total_auth=total_auth, total=total, flag=flag)
