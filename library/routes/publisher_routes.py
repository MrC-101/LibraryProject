from flask import redirect, url_for, request, render_template, Blueprint
from library.extensions import db
from library.models import Book, Author, Publisher
from library.forms import AddPublisherForm, EditPublisherForm, LimitForm
from library.maintenance import vacuum
import operator
from sqlalchemy import func

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
    books = publisher.books
    books.sort(key=operator.attrgetter('author', 'title', 'first_publish')) 
    publisher_total = len(books)
    
    return render_template('publishers/publisher_bibliography.html', books=books, publisher=publisher.publ_name, publisher_total=publisher_total, publisher_id=publisher.id)

@publisher_bp.route('/add_publisher', methods=['GET', 'POST'])
def add_publisher():
    form = AddPublisherForm()
    if form.validate_on_submit():
        publ_name = request.form['publname']
        publ_name_ret = request.form['publname']
        publ_founder = request.form['publfounder']
        publ_parent = request.form['publparent']
        publ_est = request.form['publest']
        publ_closed = request.form['publclosed']
        publ_country = request.form['publcountry']
        publ_city = request.form['publcity']
        publ_address = request.form['publaddress']
        publ_email = request.form['publemail']
        publ_website = request.form['publwebsite']
        publ_summary = request.form['publsummary']
        if not Publisher.query.filter_by(publ_name=publ_name).first():
            new_publisher = Publisher(publ_name=publ_name, publ_founder=publ_founder, publ_parent=publ_parent, publ_est=publ_est, publ_closed=publ_closed, publ_country=publ_country, publ_city=publ_city, publ_address=publ_address, publ_email=publ_email, publ_website=publ_website, publ_summary=publ_summary)
        
            db.session.add(new_publisher)
            db.session.commit()
            
            # DB VACUUM
            vacuum()
        
            publisher=db.session.query(Publisher).filter_by(publ_name=publ_name_ret).first()
            return redirect(url_for('publisher.publisher_details', id=publisher.id))
        else:
            msg='Publisher is already in the database'
            return render_template('publishers/add_publisher.html', form=form, msg=msg)
    else:
        return render_template('publishers/add_publisher.html', form=form)

@publisher_bp.route('/edit_publisher', methods=['GET', 'POST'])
def edit_publisher():
    id = request.args.get('id')
    publisher = Publisher.query.get(id)
    form = EditPublisherForm(publsummary=publisher.publ_summary)

    if form.validate_on_submit():
        publisher.publ_name = request.form['publname']
        publisher.publ_founder = request.form['publfounder']
        publisher.publ_parent = request.form['publparent']
        publisher.publ_est = request.form['publest']
        publisher.publ_closed = request.form['publclosed']
        publisher.publ_country = request.form['publcountry']
        publisher.publ_city = request.form['publcity']
        publisher.publ_address = request.form['publaddress']
        publisher.publ_email = request.form['publemail']
        publisher.publ_website = request.form['publwebsite']
        publisher.publ_summary = request.form['publsummary']
        db.session.commit()
            
        # DB VACUUM
        vacuum()
            
        return redirect(url_for('publisher.publisher_details', id=publisher.id))

    return render_template('publishers/edit_publisher.html', id=id, form=form, publisher=publisher)    
            
@publisher_bp.route('/publisher_details/<int:id>')
def publisher_details(id):
    publisher = db.session.query(Publisher).get(id)
    return render_template('publishers/publisher_details.html', publisher=publisher)

@publisher_bp.route('/publishers_by_letter', methods=['GET', 'POST'])
def publishers_by_letter():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    form = LimitForm()
    letter=request.args.get('letter')
    authors = db.session.query(Author).all()
    total_auth = len(authors)
    books = db.session.query(Book).all()
    total = len(books)
    total_publishers = len(db.session.query(Publisher).all())
    limit=form.limit.data
    # if limit != None and limit != 'None' and limit != '' and limit != '0':
    #     if letter != '*':
    #         publishers_by_letter = db.session.query(Publisher).filter(Publisher.publ_name.istartswith(letter)).order_by(func.lower(Publisher.publ_name)).limit(lim).all()
    #     else:
    #         publishers_by_letter = db.session.query(Publisher).order_by(func.lower(Publisher.publ_name)).limit(lim).all()
    # else:
    if letter != '*':
        publishers_by_letter = db.session.query(Publisher).filter(Publisher.publ_name.istartswith(letter)).order_by(func.lower(Publisher.publ_name)).all()
    else:
        publishers_by_letter = db.session.query(Publisher).order_by(func.lower(Publisher.publ_name)).all()
            
    flag='publishers_by_letter'
    choice = publishers_by_letter
    not_show_limit=True
    return render_template('index.html', flag=flag, publishers_by_letter=publishers_by_letter, total=total, total_auth=total_auth, total_publishers=total_publishers, letter=letter, letters=letters, form=form, choice=choice, not_show_limit=not_show_limit)

@publisher_bp.route('/delete_publisher/<int:id>', methods=['GET', 'POST'])
def delete_publisher(id):
    publisher = db.session.query(Publisher).get(id)
    db.session.delete(publisher)
    db.session.commit()
    
    # DB VACUUM
    vacuum()

    return redirect(url_for('main.home', flag='publishers_list'))
