from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author
from library.forms import AddAuthorForm, EditAuthorForm

author_bp = Blueprint('author',__name__)

@author_bp.route('/bibliography', methods=['GET', 'POST'])
def bibliography():
    books = db.session.query(Book).all()
    total = len(books)
    authors = Author.query.all()
    total_auth = len(authors)
    
    author = request.args.get('author')
   
    author_obj = Author.query.filter_by(fullname=author).first()
    author_id = int(author_obj.id)
    print('int id:',author_id)
    books = Book.query.filter_by(author=author).order_by('first_publish', 'title').all()
    author_total = len(books)
    return render_template('authors/bibliography.html', books=books, author=author, total=total, author_total=author_total, total_auth=total_auth, author_id=author_id)

@author_bp.route('/add_author', methods=['GET', 'POST'])
def add_author():
    form = AddAuthorForm()
    if form.validate_on_submit():
        name = request.form['name']
        country = request.form['country']
        # author_obj = Author.query.filter_by(fullname=author).first()
        born = request.form['born']
        died = form.died.data
        email = form.email.data
        bio = form.bio.data
        if not Author.query.filter_by(fullname=name, country=country, born=born).first():
            new_author = Author(fullname=name, country=country, born=born, died=died, email=email, bio=bio)
            db.session.add(new_author)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('This author is already in the library.')
    else:
        return render_template('authors/add_author.html', form=form)
    
@author_bp.route('/edit_author', methods=['GET', 'POST'])
def edit_author():
    form = EditAuthorForm()
    id = request.args.get('id')
    print(id)
    author = Author.query.get(id)
    print(author.fullname)
    if author.bio:
        form.bio.data=author.bio
    if form.validate_on_submit():
        print('after POST',author.fullname)
        if author:
            author.fullname = form.name.data
            author.country = form.country.data
            author.born = form.born.data
            author.died = form.died.data
            author.email = form.email.data
            author.bio = request.form['bio']
        
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            print('author not found!!!!!!!!!')

    return render_template('authors/edit_author.html', id=id, form=form, author=author)