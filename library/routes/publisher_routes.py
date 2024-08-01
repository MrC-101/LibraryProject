from flask import redirect, url_for, request, render_template, flash, Blueprint
from library.extensions import db
from library.models import Book, Author, Publisher
from library.forms import AddPublisherForm, EditPublisherForm
from library.maintenance import vacuum
import operator

publisher_bp = Blueprint('publisher',__name__)

@publisher_bp.route('/publisher_authors')
def publisher_authors():
    publisher = request.args.get('publisher')
    publisher = Publisher.query.filter_by(publ_name=publisher).first()
    authors = publisher.authors
    publisher_total = len(publisher.authors)
    return render_template('publishers/publisher_authors.html', publisher=publisher.publ_name, publisher_total=publisher_total, publisher_id=publisher.id, authors=authors)

@publisher_bp.route('/publisher_bibliography', methods=['GET', 'POST'])
def publisher_bibliography():
    publisher = request.args.get('publisher')
    publisher = Publisher.query.filter_by(publ_name=publisher).first()
    publisher_id = int(publisher.id)
    # books = Book.query.filter_by(author=author).order_by('first_publish', 'title').all()
    # publisher = db.session.query(Publisher).filter_by(publ_name=publisher).first()
    
    books = publisher.books
    books.sort(key=operator.attrgetter('author', 'title', 'first_publish')) 
    
    publisher_total = len(books)
    return render_template('publishers/publisher_bibliography.html', books=books, publisher=publisher.publ_name, publisher_total=publisher_total, publisher_id=publisher_id)

@publisher_bp.route('/add_publisher', methods=['GET', 'POST'])
def add_publisher():
    form = AddPublisherForm()
    if form.validate_on_submit():
        publ_name = request.form['publname']
        publ_name_ret = request.form['publname']
        publ_founder = request.form['publfounder']
        publ_parent = request.form['publparent']
        publ_est = request.form['publest']
        publ_country = request.form['publcountry']
        publ_city = request.form['publcity']
        publ_address = request.form['publaddress']
        publ_email = request.form['publemail']
        publ_website = request.form['publwebsite']
        if not Publisher.query.filter_by(publ_name=publ_name).first():
            new_publisher = Publisher(publ_name=publ_name, publ_founder=publ_founder, publ_parent=publ_parent, publ_est=publ_est, publ_country=publ_country, publ_city=publ_city, publ_address=publ_address, publ_email=publ_email, publ_website=publ_website)
        
            db.session.add(new_publisher)
            db.session.commit()
            
            # DB VACUUM ANALYZE
            vacuum()
        
            publisher=db.session.query(Publisher).filter_by(publ_name=publ_name_ret).first()
            return redirect(url_for('publisher.publisher_details', id=publisher.id))
        else:
            flash('This publisher is already in the library.')
    else:
        return render_template('publishers/add_publisher.html', form=form)

@publisher_bp.route('/edit_publisher', methods=['GET', 'POST'])
def edit_publisher():
    id = request.args.get('id')
    publisher = Publisher.query.get(id)
    form = EditPublisherForm()

    if form.validate_on_submit():
        publisher.publ_name = request.form['publname']
        publisher.publ_founder = request.form['publfounder']
        publisher.publ_parent = request.form['publparent']
        publisher.publ_est = request.form['publest']
        publisher.publ_country = request.form['publcountry']
        publisher.publ_city = request.form['publcity']
        publisher.publ_address = request.form['publaddress']
        publisher.publ_email = request.form['publemail']
        publisher.publ_website = request.form['publwebsite']
        db.session.commit()
            
        # DB VACUUM ANALYZE
        vacuum()
            
        return redirect(url_for('publisher.publisher_details', id=publisher.id))

    return render_template('publishers/edit_publisher.html', id=id, form=form, publisher=publisher)    
            
@publisher_bp.route('/publisher_details/<int:id>')
def publisher_details(id):
    publisher = db.session.query(Publisher).get(id)
    return render_template('publishers/publisher_details.html', publisher=publisher)

@publisher_bp.route('/publishers_by_letter')
def publishers_by_letter():
    letter=request.args.get('letter')
    authors = db.session.query(Author).all()
    total_auth = len(authors)
    books = db.session.query(Book).all()
    total = len(books)
    publishers = db.session.query(Publisher).all()
    total_publishers = len(publishers)
    if letter != '*':
        publishers_by_letter = db.session.query(Publisher).filter(Publisher.publ_name.istartswith(letter)).all()
    else:
        publishers_by_letter = db.session.query(Publisher).order_by('publ_name').all()
    return render_template('index.html', flag='publishers_by_letter', publishers_by_letter=publishers_by_letter, total=total, total_auth=total_auth, total_publishers=total_publishers)