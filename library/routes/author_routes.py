from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Author, Book
from library.forms import AddAuthorForm, EditAuthorForm
import operator, select

author_bp = Blueprint('author',__name__)

@author_bp.route('/bibliography', methods=['GET', 'POST'])
def bibliography():
    author = request.args.get('author')
    author_obj = Author.query.filter_by(fullname=author).first()
    author_id = int(author_obj.id)
    # books = Book.query.filter_by(author=author).order_by('first_publish', 'title').all()
    author = db.session.query(Author).filter_by(fullname=author).first()
    
    books = author.books
    books.sort(key=operator.attrgetter('first_publish', 'title')) 
    
    author_total = len(books)
    return render_template('authors/bibliography.html', books=books, author=author.fullname, author_total=author_total, author_id=author_id)

@author_bp.route('/add_author', methods=['GET', 'POST'])
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        name_pref = form.name_pref.data
        fname = request.form['fname']
        midname = request.form['midname']
        lname = request.form['lname']
        name_suf = form.name_suf.data
        gender = form.gender.data
        if midname != '' and midname != None and midname != 'None':
            if fname != '' and fname != None:
                fullname = fname + ' ' + midname + ' ' + lname
            else:
                fullname = fname
        else:
            if fname != '' and fname != None and fname != 'None':
                fullname = fname + ' ' + lname
            else: 
                fullname = fname
        country = request.form['country']
        city = request.form['city']
        born = request.form['born']
        died = form.died.data
        email = form.email.data
        bio = form.bio.data
        if not Author.query.filter_by(lname=lname, fname=fname, country=country, born=born).first():
            new_author = Author(name_pref=name_pref, fname=fname, lname=lname, name_suf=name_suf, gender=gender, fullname=fullname, country=country, city=city, born=born, died=died, email=email, bio=bio)
            db.session.add(new_author)
            id=new_author.id
            db.session.commit()
            return redirect(url_for('author.author_details', id=id))
        else:
            flash('This author is already in the library.')
    else:
        return render_template('authors/add_author.html', form=form)
    
@author_bp.route('/edit_author', methods=['GET', 'POST'])
def edit_author():
    id = request.args.get('id')
    author = Author.query.get(id)
    form = EditAuthorForm(gender=author.gender, bio=author.bio)

    if form.validate_on_submit():
        if author:
            author.name_pref = form.name_pref.data
            author.fname = form.fname.data
            author.midname = form.midname.data
            author.lname = form.lname.data
            author.name_suf = form.name_suf.data
            author.gender = form.gender.data
            if author.midname != '' and author.midname != None and author.midname != 'None':
                if author.fname != '' and author.fname != None and author.fname != 'None':
                    author.fullname = author.fname + ' ' + author.midname + ' ' + author.lname
                else:
                    author.fullname = author.lname
            else:
                if author.fname != '' and author.fname != None and author.fname != 'None':
                    author.fullname = author.fname + ' ' + author.lname
                else:
                    author.fullname = author.lname
            author.country = form.country.data
            author.city = form.city.data
            author.born = form.born.data
            author.died = form.died.data
            author.email = form.email.data
            author.bio = request.form['bio']
        
            db.session.commit()
            return redirect(url_for('author.author_details', id=author.id))

    return render_template('authors/edit_author.html', id=id, form=form, author=author)

@author_bp.route('/delete_author/<int:id>', methods=['GET', 'POST'])
def delete_author(id):
    author = db.session.query(Author).get(id)
    for book in author.books:
        if len(book.authors) == 1:
            db.session.delete(book)
            db.session.commit()
    for book in author.books:
        book.authors.remove(author)
        book.author = book.authors[0].fullname
        book.co_author = author.fullname        
        db.session.commit()
    db.session.delete(author)
    db.session.commit()

    return redirect(url_for('main.home', flag='authors_list'))

@author_bp.route('/author_details/<int:id>')
def author_details(id):
    author = db.session.query(Author).get(id)
    return render_template('authors/author_details.html', author=author)

@author_bp.route('/authors_by_leter')
def authors_by_letter():
    letter=request.args.get('letter')
    authors = db.session.query(Author).all()
    total_auth = len(authors)
    books = db.session.query(Book).all()
    total = len(books)
    if letter != '*':
        authors_by_letter = db.session.query(Author).filter(Author.lname.istartswith(letter)).all()
    else:
        authors_by_letter = db.session.query(Author).order_by('fullname').all()
    return render_template('index.html', flag='authors_by_letter', authors_by_letter=authors_by_letter, total=total, total_auth=total_auth)