from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import SearchAllItemsForm, SearchAuthorsForm, SearchBooksForm
import operator, time
from sqlalchemy import or_
from library.maintenance import vacuum

main_bp = Blueprint('main',__name__)

@main_bp.route('/init')
def init():
    
    vacuum()    

    # # db.create_all()
    
    # authors=[
    #       Author(fullname='Gabriel García Márquez'),
    #       Author(fullname='Umberto Eco'),
    #       Author(fullname='William Faulkner'),
    # ]
    
    # for author in authors:
    #     db.session.add(author)
    #     db.session.commit()

    # book=Book(title="The 10th Commandment", author='Elena Alpha', first_publish=2005, isbn='123456780X', rating=9.9, authors=[author])
    # db.session.add(book)

    # author.books.append(book)

    
    # elena = db.session.query(Author).filter_by(fullname='Elena Alpha').first()
    # books = [book.title for book in elena.books]
    # print(f"Elena's Books: {', '.join(books)}")
    
    return redirect(url_for('main.home'))

@main_bp.route('/')
def home():
    books_totals = db.session.query(Book).order_by('author', 'first_publish', 'title').all()
    authors_totals = db.session.query(Author).order_by('fullname').all()
    total_auth = len(authors_totals)
    total = len(books_totals)
    flag = request.args.get('flag')
    authors = authors_totals
    # # books=[]
    # # for author in authors:
    # #     for book in author.books:
    # #         books.append(book)
    # books=[book for author in authors for book in author.books]
    # books.sort(key=operator.attrgetter('author', 'first_publish', 'title'))
    books = books_totals
    # if flag == 'authors_list':
    return render_template('index.html', books=books, authors=authors, flag=flag, total=total, total_auth=total_auth)
    # else: 
        # return render_template('index.html', books=books, total=total, total_auth=total_auth)

@main_bp.route('/search_books', methods=['GET', 'POST'])
def search_books():

    books = db.session.query(Book).order_by('author', 'title').all()
    authors = Author.query.all()
    total_auth = len(authors)
    total = len(books)
    
    form = SearchBooksForm()
    flag = request.args.get('flag')
    
    if request.method == 'POST':
        if form.validate_on_submit():
            books = db.session.query(Book).all()
            total = len(books)
            title_returned = form.title.data
            
            if Book.query.filter_by(title=title_returned).first():
                start = time.perf_counter_ns()
                books = Book.query.filter_by(title=title_returned).order_by('author', 'title').all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if len(books) > 1:
                    form = SearchBooksForm()
                    return render_template('search_books.html', flag='books_list', form=form, books=books, duration=duration)
                else:
                    book = Book.query.filter_by(title=title_returned).first()
                    return redirect(url_for('book.edit_title', author=book.author, id=book.id, total=total, total_auth=total_auth))  
                
            elif db.session.query(Book).filter(Book.title.icontains(title_returned)).all():
                start = time.perf_counter_ns()
                books = db.session.query(Book).filter(Book.title.icontains(title_returned)).order_by('author', 'title').all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if len(books) > 1:
                    form = SearchBooksForm()
                    return render_template('search_books.html', form=form, books=books, duration=duration)
                else:
                    book = books[0]
                    return redirect(url_for('book.book_details', author=book.author, id=book.id, total=total, total_auth=total_auth)) 
                       
            else:
                flash('Nothing found in the Database')
                start = time.perf_counter_ns()
                books = Book.query.order_by('author').all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                form = SearchBooksForm()
                return render_template('search_books.html', form=form, books=books, duration=duration)
    else:
        return render_template('search_books.html', form=form, books=books, total_auth=total_auth, total=total, flag=flag)
    
@main_bp.route('/search_authors', methods=['GET', 'POST'])
def search_authors():
    books = db.session.query(Book).all()
    authors = Author.query.order_by('fullname', 'lname').all()
    total_auth = len(authors)
    total = len(books)
    duration = 0
    form = SearchAuthorsForm()
    flag = request.args.get('flag')
    if request.method == 'POST':
        if form.validate_on_submit():
            
            books = db.session.query(Book).all()
            total = len(books)
            
            author_returned = form.author.data
            
            if Author.query.filter_by(fullname=author_returned).first():
                start = time.perf_counter_ns()
                authors = Author.query.filter_by(fullname=author_returned).order_by('fullname', 'lname').all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                if len(authors) > 1:
                    form = SearchAuthorsForm()
                    return render_template('search_authors.html', flag='authors_list', form=form, authors=authors, total=total, total_auth=total_auth, duration=duration)                
                else:
                    return redirect(url_for('author.author_details', author=author_returned, id=authors[0].id))
                        
            elif db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all():
                for i in range(10):
                    print('all authors')
                authors=[]
                authors1=[]
                authors2=[]
                authors3=[]
                duration1=0
                duration2=0
                duration3=0
                   
                if db.session.query(Author).filter(Author.lname.istartswith(author_returned)).all():
                    for i in range(10):
                        print('authors1-lname')
                    start = time.perf_counter_ns()
                    authors1 = db.session.query(Author).filter(Author.lname.istartswith(author_returned)).order_by('lname','fullname').all()
                    
                    end = time.perf_counter_ns()
                    duration1 = (end - start)/1000000
                    
                if db.session.query(Author).filter(Author.fname.istartswith(author_returned)).all():
                    for i in range(10):
                        print('authors2-fname')
                    start = time.perf_counter_ns()
                    authors2 = db.session.query(Author).filter(Author.fname.istartswith(author_returned)).order_by('fullname', 'lname').all()
                    
                    end = time.perf_counter_ns()
                    duration2 = (end - start)/1000000
                    
                if db.session.query(Author).filter(Author.midname.istartswith(author_returned)).all():
                    for i in range(10):
                        print('authors3-midname')
                    start = time.perf_counter_ns()
                    authors3= db.session.query(Author).filter(Author.midname.istartswith(author_returned)).order_by('lname','fullname').all()
                    
                    end = time.perf_counter_ns()
                    duration3 = (end - start)/1000000
                    
                # if db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all():
                #     start = time.perf_counter_ns()  
                #     authors4 = db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all()
                #     end = time.perf_counter_ns()
                #     duration = str((end - start)/1000000)[:4]
                if authors1 and authors2 and authors3:  
                    for i in range(10):
                        print('all 3')      
                    authors = authors1 + authors2 + authors3
                elif authors1 and authors2:
                    for i in range(10):
                        print('1+2')
                    authors = authors1 + authors2
                elif authors1 and authors3:
                    for i in range(10):
                        print('1+3')
                    authors = authors1 + authors3
                elif authors2 and authors3:
                    for i in range(10):
                        print('2+3')
                    authors = authors2 + authors3
                elif authors1:
                    for i in range(10):
                        print('1-lname')
                    authors = authors1
                elif authors2:
                    for i in range(10):
                        print('2-fname')
                    authors = authors2
                elif authors3:
                    for i in range(10):
                        print('3-midname')
                    authors = authors3
                else:
                    start = time.perf_counter_ns()
                    flash('Nothing found in the Database. Check your spelling or try a different Name')
                    authors = Author.query.order_by('fullname').all()
                    end = time.perf_counter_ns()
                    duration = str((end - start)/1000000)[:4]
                    form = SearchAuthorsForm()
                    return render_template('search_authors.html', form=form, authors=authors, total=total, total_auth=total_auth, duration=duration)
                    
                duration = str(duration1+duration2+duration3)[:4]
                
                if authors:
                    if len(authors) > 1:
                        for i in range(10):
                            print('authors list')
                        # return redirect(url_for('main.search_authors', flag='authors_list', form=form, authors=authors, total=total, total_auth=total_auth, duration=duration))
                        return render_template('search_authors.html', form=form, authors=authors, duration=duration)
                    else:
                        author = authors[0]
                        return redirect(url_for('author.author_details', author=author, id=author.id, total=total, total_auth=total_auth))                    
     
            else:
                start = time.perf_counter_ns()
                flash('Nothing found in the Database. Check your spelling or try a different Name')
                authors = Author.query.order_by('fullname').all()
                end = time.perf_counter_ns()
                duration = str((end - start)/1000000)[:4]
                form = SearchAuthorsForm()
                return render_template('search_authors.html', form=form, authors=authors, total=total, total_auth=total_auth, duration=duration)
    else:
        for i in range(10):
            print('in here !!!')
        return render_template('search_authors.html', form=form, authors=authors, total_auth=total_auth, total=total, flag=flag)
       
@main_bp.route('/search_all', methods=["GET", "POST"])
def search_all():
    start = time.perf_counter_ns()
    authors = db.session.query(Author).order_by('fullname').all()
    books = db.session.query(Book).order_by('title', 'author', 'first_publish').all()
    end = time.perf_counter_ns()
    duration = str((end - start)/1000000)[:4]
    form = SearchAllItemsForm()
    if form.validate_on_submit():
        authors.clear()
        books.clear() 
        start = time.perf_counter_ns()
          
        all_items = form.all_items.data
        form.all_items.data = ''
        
        authors = db.session.query(Author).filter(or_ (Author.fullname.icontains(all_items), Author.died.icontains(all_items), Author.born.icontains(all_items), Author.country.icontains(all_items), Author.city.icontains(all_items), Author.penname.icontains(all_items))).all()
        books = db.session.query(Book).filter(or_ (Book.title.icontains(all_items), Book.summary.icontains(all_items), Book.genre.icontains(all_items), Book.first_publish.icontains(all_items))).all()
        
        end = time.perf_counter_ns()
        duration = str((end - start)/1000000)[:4]
        
        if authors and books:            
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, books=books, duration=duration)
        elif authors:
            return render_template('search_all.html', form=SearchAllItemsForm(), authors=authors, duration=duration)
        elif books:
            return render_template('search_all.html', form=SearchAllItemsForm(), books=books, duration=duration)
        else:
            flash('Nothing found in the database')
        
        
    return render_template('search_all.html', form=form, authors=authors, duration=duration)        
              
# @main_bp.route('/search', methods=['GET', 'POST'])
# def search():
#     books = db.session.query(Book).all()
#     authors = Author.query.all()
#     total_auth = len(authors)
#     total = len(books)
#     form = SearchForm()
#     flag = request.args.get('flag')
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             books = db.session.query(Book).all()
#             total = len(books)
#             title_returned = form.title.data
#             author_returned = form.author.data
#             isbn10_returned = form.isbn10.data
#             isbn13_returned = form.isbn13.data
#             form.title.data = ''
#             form.author.data = ''
#             form.isbn10.data = ''
#             form.isbn13.data = ''
            
#             if Book.query.filter_by(title=title_returned, author=author_returned).first():
#                 book = Book.query.filter_by(title=title_returned).filter_by(author=author_returned).first()
#                 return redirect(url_for('book.edit_title', id=book.id, total=total, total_auth=total_auth))
            
#             elif Book.query.filter_by(title=title_returned).first() and not Book.query.filter_by(author=author_returned).first():
#                 books = Book.query.filter_by(title=title_returned).all()
#                 if len(books) > 1:
#                     form = SearchForm()
#                     return render_template('search.html', flag='books_list', form=form, books=books, total=total, total_auth=total_auth)
#                 else:
#                     book = Book.query.filter_by(title=title_returned).first()
#                     return redirect(url_for('book.edit_title', author=book.author, id=book.id, total=total, total_auth=total_auth))
            
#             elif Book.query.filter_by(author=author_returned).first() and not Book.query.filter_by(title=title_returned).first() or Author.query.filter_by(fullname=author_returned).first():
#                 author_obj = Author.query.filter_by(fullname=author_returned).first()
#                 books = Book.query.filter_by(author=author_returned).all()
          
#                 if len(books) > 1:
#                     form = SearchForm()
#                     for _ in range(10):
#                         print('here here 1')
#                     return redirect(url_for('author.bibliography', author=author_returned, author_id=author_obj.id, form=form, books=books, total=total, total_auth=total_auth))
                
#                 elif len(books) == 1:
#                     book = Book.query.filter_by(author=author_returned).first()
#                     return redirect(url_for('book.edit_title', author=author_returned, author_id=author_obj.id, id=book.id, total=total, total_auth=total_auth))
                
#                 else:
#                     return redirect(url_for('author.edit_author', author=author_returned, id=author_obj.id))
                
#             elif db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all() and title_returned == '':
#                 for _ in range(10):
#                     print('We are in!!!!!!!!!!')
#                 authors = db.session.query(Author).filter(Author.fullname.icontains(author_returned)).all()
#                 if len(authors) > 1:
#                     for _ in range(10):
#                         print('Many Authors')
#                     form = SearchForm()
#                     return render_template('search_authors.html', flag='authors_list', form=form, authors=authors, total=total, total_auth=total_auth)
#                 else:
#                     for _ in range(10):
#                         print('One Author')
#                     author = authors[0]
#                     return redirect(url_for('author.author_details', author=author, id=author.id, total=total, total_auth=total_auth))       
                
#             elif db.session.query(Book).filter(Book.title.icontains(title_returned)).all():
#                 books = db.session.query(Book).filter(Book.title.icontains(title_returned)).all()
#                 if len(books) > 1:
#                     form = SearchForm()
#                     return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
#                 else:
#                     book = books[0]
#                     return redirect(url_for('book.book_details', author=book.author, id=book.id, total=total, total_auth=total_auth)) 
                
#             elif Book.query.filter_by(isbn10=isbn10_returned) and isbn10_returned is not '':
#                 book = Book.query.filter_by(isbn10=isbn10_returned).first()
#                 return redirect(url_for('author.bibliography', author=book.author))
 
#             elif Book.query.filter_by(isbn13=isbn13_returned) and isbn13_returned is not '':
#                 book = Book.query.filter_by(isbn13=isbn13_returned).first()
#                 return redirect(url_for('author.bibliography', author=book.author))
                       
#             else:
#                 flash('Nothing found in the Database')
#                 books = Book.query.order_by('author').all()
#                 form = SearchForm()
#                 return render_template('search.html', form=form, books=books, total=total, total_auth=total_auth)
#     else:
#         return render_template('search.html', form=form, books=books, total_auth=total_auth, total=total, flag=flag)
