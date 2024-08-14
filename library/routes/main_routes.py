from flask import redirect, url_for, request, render_template, Blueprint
from library.extensions import db
from library.models import Book, Author, Publisher
from library.forms import SearchAllItemsForm, SearchAuthorsForm, SearchBooksForm, LimitForm, SearchPublishersForm
import operator, time
from sqlalchemy import or_, func

main_bp = Blueprint('main',__name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    form=LimitForm()
    limit = 0
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if form.validate_on_submit():
        limit = request.form.get('limit')
        if limit != '' and limit != None:
            limit = int(limit)
        else:
            limit = 0
    else:
        limit = 0
    books_totals = db.session.query(Book).order_by(func.lower(Book.author), func.lower(Book.first_publish), func.lower(Book.title)).all()
    authors_totals = db.session.query(Author).order_by(func.lower(Author.lname)).all()
    publishers_totals = db.session.query(Publisher).order_by(func.lower(Publisher.publ_name)).all()
    flag = request.args.get('flag')
    authors = authors_totals
    publishers = publishers_totals
    total_books = len(db.session.query(Book).all())
    total_auth = len(db.session.query(Author).all())
    total_publishers = len(db.session.query(Publisher).all())

    # # books=[]
    # # for author in authors:
    # #     for book in author.books:
    # #         books.append(book)
    # books=[book for author in authors for book in author.books]
    # books.sort(key=operator.attrgetter('author', 'first_publish', 'title'))
    books = books_totals
    choice = publishers
    if flag == None:
        flag = 'books_list'
        info = "Flag was set to None. Auto switched to 'books_list'"
        print('\n'+'=' * len(info))
        print(info)
        print('=' * len(info)+'\n')
        
    not_show_limit=True if flag == 'publishers_list' or flag == 'publishers_by_letter' else False
                
    return render_template('index.html', books=books, authors=authors, publishers=publishers, flag=flag, total=total_books, total_auth=total_auth, limit=limit, total_publishers=total_publishers, form=form, letters=letters, choice=choice, not_show_limit=not_show_limit)

@main_bp.route('/search_books', methods=['GET', 'POST'])
def search_books():
    books = db.session.query(Book).order_by(func.lower(Book.author), func.lower(Book.title)).all()
    authors = Author.query.all()
    total_auth = len(authors)
    total = len(books)
    msg = 'No Book found. Check your spelling.'
    form = SearchBooksForm()
    flag = request.args.get('flag')
    authors_count = len(set(authors))

    if request.method == 'POST':
        if form.validate_on_submit():
            books = db.session.query(Book).all()
            authors = Author.query.order_by(func.lower(Author.knownas)).all()
            total = len(books)
            title_returned = form.title.data
            if title_returned == '' or title_returned == None:
                msg = 'Please enter a book title or part of it, to search for...'
                return render_template('search_books.html', form=form, books=books, total_auth=total_auth, total=total, flag=flag, authors_count=authors_count, msg=msg)
            
            if Book.query.filter_by(title=title_returned).first():
                start = time.perf_counter_ns()
                books = Book.query.filter_by(title=title_returned).order_by(func.lower(Book.author), func.lower(Book.title), func.lower(Book.first_publish)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if len(books) > 1:
                    form = SearchBooksForm()
                    authors_count = len(set([book.author for book in books]))
                    return render_template('search_books.html', flag='books_list', form=form, books=books, duration=duration, authors_count=authors_count, authors=authors)
                else:
                    book = Book.query.filter_by(title=title_returned).first()
                    return redirect(url_for('book.edit_title', author=book.author, id=book.id, total=total, total_auth=total_auth))  
                
            elif db.session.query(Book).filter(Book.title.icontains(title_returned)).all():
                start = time.perf_counter_ns()
                books = db.session.query(Book).filter(Book.title.icontains(title_returned)).order_by(func.lower(Book.author), func.lower(Book.title), func.lower(Book.first_publish)).all()
                
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]

                if len(books) > 1:
                    authors_count = len(set([book.author for book in books]))
                    form = SearchBooksForm()
                    return render_template('search_books.html', form=form, books=books, authors=authors, duration=duration, authors_count=authors_count)
                else:
                    book = books[0]
                    return redirect(url_for('book.book_details', author=book.author, id=book.id, total=total, total_auth=total_auth)) 
            else:
                start = time.perf_counter_ns()
                books = Book.query.order_by(func.lower(Book.author), func.lower(Book.title), func.lower(Book.first_publish)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                form = SearchBooksForm()
                return render_template('search_books.html', form=form, authors=authors, books=books, duration=duration, msg=msg)
    else:
        return render_template('search_books.html', form=form, books=books, authors=authors, total_auth=total_auth, total=total, flag=flag, authors_count=authors_count)
    
@main_bp.route('/search_authors', methods=['GET', 'POST'])
def search_authors():
    books = db.session.query(Book).all()
    authors = Author.query.order_by(func.lower(Author.lname), func.lower(Author.lname)).all()
    total_auth = len(authors)
    total = len(books)
    duration = 0
    msg ='No Authors found. Check your spelling.'
    form = SearchAuthorsForm()
    flag = 'authors_list'

    if request.method == 'POST':
        if form.validate_on_submit():
            books = db.session.query(Book).all()
            total = len(books)
            author_returned = form.author.data
            
            if author_returned == '' or author_returned == None:
                msg = 'Please enter an author name or part of it, to search for...'
                return render_template('search_authors.html', form=form, authors=authors, total_auth=total_auth, total=total, flag=flag, msg=msg)
    
            if Author.query.filter_by(fullname=author_returned).first():
                start = time.perf_counter_ns()
                authors = Author.query.filter_by(fullname=author_returned).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if len(authors) > 1:
                    form = SearchAuthorsForm()
                    return render_template('search_authors.html', flag='authors_list', form=form, authors=authors, total=total, total_auth=total_auth, duration=duration)
                else:
                    return redirect(url_for('author.author_details', author=author_returned, id=authors[0].id))
                        
            elif db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all():
                
                #Lists creation
                authors=[]
                authors1=[]
                authors2=[]
                authors3=[]
                
                duration1=0
                duration2=0
                duration3=0

                if db.session.query(Author).filter(Author.lname.icontains(author_returned)).all():
                    start = time.perf_counter_ns()
                    authors1 = db.session.query(Author).filter(Author.lname.icontains(author_returned)).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                    end = time.perf_counter_ns()
                    duration1 = (end - start)/1000000

                if db.session.query(Author).filter(Author.fname.icontains(author_returned)).all():
                    start = time.perf_counter_ns()
                    authors2 = db.session.query(Author).filter(Author.fname.icontains(author_returned)).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                    end = time.perf_counter_ns()
                    duration2 = (end - start)/1000000

                if db.session.query(Author).filter(Author.midname.icontains(author_returned)).all():
                    start = time.perf_counter_ns()
                    authors3= db.session.query(Author).filter(Author.midname.icontains(author_returned)).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                    end = time.perf_counter_ns()
                    duration3 = (end - start)/1000000

                if authors1 and authors2 and authors3:
                    authors = authors1 + authors2 + authors3
                elif authors1 and authors2:
                    authors = authors1 + authors2
                elif authors1 and authors3:
                    authors = authors1 + authors3
                elif authors2 and authors3:
                    authors = authors2 + authors3
                elif authors1:
                    authors = authors1
                elif authors2:
                    authors = authors2
                elif authors3:
                    authors = authors3
                else:
                    start = time.perf_counter_ns()
                    authors = Author.query.order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                    end = time.perf_counter_ns()
                    duration = str((end - start)/1000000)[:4]
                    form = SearchAuthorsForm()
                    return render_template('search_authors.html', form=form, authors=authors, flag=flag, total=total, total_auth=total_auth, duration=duration, msg=msg)
                    
                duration = str(duration1+duration2+duration3)[:4]
                
                if authors:
                    if len(authors) > 1:
                        return render_template('search_authors.html', form=form, authors=authors, flag=flag, duration=duration)
                    else:
                        author = authors[0]
                        return redirect(url_for('author.author_details', author=author, id=author.id, total=total, flag=flag, total_auth=total_auth))

            elif db.session.query(Author).filter(Author.knownas.icontains(author_returned)).all():
                start = time.perf_counter_ns()
                authors = db.session.query(Author).filter(Author.knownas.icontains(author_returned)).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                end = time.perf_counter_ns()
                duration = (end - start)/1000000
                if authors:
                    if len(authors) > 1:
                        return render_template('search_authors.html', form=form, authors=authors, flag=flag, duration=duration)
                    else:
                        author = authors[0]
                        return redirect(url_for('author.author_details', author=author, id=author.id, total=total, flag=flag, total_auth=total_auth))

            elif db.session.query(Author).filter(Author.penname.icontains(author_returned)).all():
                start = time.perf_counter_ns()
                authors = db.session.query(Author).filter(Author.penname.icontains(author_returned)).order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                end = time.perf_counter_ns()
                duration = (end - start)/1000000
                if authors:
                    if len(authors) > 1:
                        return render_template('search_authors.html', form=form, authors=authors, flag=flag, duration=duration)
                    else:
                        author = authors[0]
                        return redirect(url_for('author.author_details', author=author, id=author.id, total=total, flag=flag, total_auth=total_auth)) 
                        
            else:
                start = time.perf_counter_ns()      
                authors = Author.query.order_by(func.lower(Author.fullname), func.lower(Author.lname)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                form = SearchAuthorsForm()
                return render_template('search_authors.html', flag=flag, form=form, authors=authors, total=total, total_auth=total_auth, duration=duration, msg=msg)
                
    else:
        return render_template('search_authors.html', form=form, authors=authors, total_auth=total_auth, total=total, flag=flag)

@main_bp.route('/search_publishers', methods=['GET', 'POST'])
def search_publishers():
    publishers = Publisher.query.order_by('publ_name').all()
    duration = 0
    msg='No Publishers found. Check your spelling.'
    form = SearchPublishersForm()
    flag = request.args.get('flag')
    if request.method == 'POST':
        if form.validate_on_submit():
            
            publisher_returned = form.publisher.data
            if publisher_returned == '' or publisher_returned == None:
                msg = 'Please enter a publisher name or part of it, to search for...'
                return render_template('search_publishers.html', form=form, publishers=publishers, flag=flag, msg=msg)
            
            if Publisher.query.filter_by(publ_name=publisher_returned).first():
                start = time.perf_counter_ns()
                publisher = Publisher.query.filter_by(publ_name=publisher_returned).first()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                return redirect(url_for('publisher.publisher_details', publisher=publisher, id=publisher.id))
            
            elif db.session.query(Publisher).filter(Publisher.publ_name.istartswith(publisher_returned)).all():
                start = time.perf_counter_ns()
                publishers = db.session.query(Publisher).filter(Publisher.publ_name.istartswith(publisher_returned)).order_by(func.lower(Publisher.publ_name)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if publishers:
                    if len(publishers) > 1:
                        return render_template('search_publishers.html', form=form, publishers=publishers, duration=duration)
                    else:
                        publisher = publishers[0]
                        return redirect(url_for('publisher.publisher_details', form=form, publisher=publisher, id=publisher.id))
                                
            elif db.session.query(Publisher).filter(Publisher.publ_name.icontains(publisher_returned)).all():
                start = time.perf_counter_ns()
                publishers = db.session.query(Publisher).filter(Publisher.publ_name.icontains(publisher_returned)).order_by(func.lower(Publisher.publ_name)).all()                    
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if publishers:
                    if len(publishers) > 1:
                        return render_template('search_publishers.html', form=form, publishers=publishers, duration=duration)
                    else:
                        publisher = publishers[0]
                        return redirect(url_for('publisher.publisher_details', form=form, publisher=publisher, id=publisher.id))      
            else:
                start = time.perf_counter_ns()
                publishers = Publisher.query.order_by(func.lower(Publisher.publ_name)).all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                form = SearchPublishersForm()
                return render_template('search_publishers.html', form=form, publishers=publishers, duration=duration, msg=msg)

    else:
        return render_template('search_publishers.html', form=form, publishers=publishers, flag=flag)

@main_bp.route('/search_all', methods=["GET", "POST"])
def search_all():
    start = time.perf_counter_ns()
    authors = db.session.query(Author).order_by(func.lower(Author.fullname)).limit(3).all()
    books = db.session.query(Book).order_by(func.lower(Book.title), func.lower(Book.author), func.lower(Book.first_publish)).limit(3).all()
    publishers = Publisher.query.order_by(func.lower(Publisher.publ_name)).limit(3).all()
    books_count = len(Book.query.all())
    authors_count = len(Author.query.all())
    publishers_count = len(Publisher.query.all())
    end = time.perf_counter_ns()
    duration = str((end - start)/1000000)[:4]
    msg = 'Nothing found. Check your spelling.'
    form = SearchAllItemsForm()

    if form.validate_on_submit():
        authors.clear()
        books.clear()
        publishers.clear()
        all_items = request.form['all_items']
        form.all_items.data = ''
        if all_items == '' or all_items == None:
            msg = 'Please enter something to search for...' 
            return render_template('search_all.html', form=form, authors=authors, books=books, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count, msg=msg)
        
        start = time.perf_counter_ns()
        
        authors = db.session.query(Author).filter(or_ (Author.fullname.icontains(all_items), Author.died.icontains(all_items), Author.born.icontains(all_items), Author.country.icontains(all_items), Author.penname.icontains(all_items), Author.knownas.icontains(all_items))).order_by(func.lower(Author.fullname)).all()
        
        books = db.session.query(Book).filter(or_ (Book.title.icontains(all_items), Book.first_publish.icontains(all_items))).order_by(func.lower(Book.title), func.lower(Book.author)).all()
        
        if books:
            authors_in_book_list = [Author.query.filter_by(fullname=book.author).first() for book in books]
        
        publishers = db.session.query(Publisher).filter(or_ (Publisher.publ_name.icontains(all_items), Publisher.publ_est.icontains(all_items), Publisher.publ_country.icontains(all_items), Publisher.publ_parent.icontains(all_items))).order_by(func.lower(Publisher.publ_name)).all()
        
        end = time.perf_counter_ns()
        duration = str((end - start)/1000000)[:4]

        books_count = len(books)
        authors_count = len(authors)
        publishers_count = len(publishers)
        
        if authors and books and publishers:
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, authors_in_book_list=authors_in_book_list, books=books, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif authors and books:
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, authors_in_book_list=authors_in_book_list, books=books, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif authors and publishers:
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif books and publishers:
            return render_template('search_all.html', form=SearchAllItemsForm(), books=books, authors_in_book_list=authors_in_book_list, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif authors:
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif books: 
            print(len(authors))
            return render_template('search_all.html', form=SearchAllItemsForm(), books=books, authors_in_book_list=authors_in_book_list, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        elif publishers:
            return render_template('search_all.html', form=SearchAllItemsForm(), publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
        else:
            msg = 'Nothing relevant found in the database.'
            return render_template('search_all.html', form=form, authors=authors, books=books, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count, msg=msg)
        
    return render_template('search_all.html', form=form, authors=authors, books=books, publishers=publishers, duration=duration, books_count=books_count, authors_count=authors_count, publishers_count=publishers_count)
