from flask import redirect, url_for, render_template, Blueprint
import operator, time
from sqlalchemy import or_,  func
from library.maintenance import vacuum_analyze, vacuum_full, vacuum
from library.models import Author, Book, Publisher
from library.extensions import db

maintenance_bp = Blueprint('maintenance',__name__)

@maintenance_bp.route('/init')
def init():
    
    # publishers = Publisher.query.all()
    # letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # publets=[]
    # for letter in letters:
    #     for publisher in publishers:
    #         publets.append((publisher.publ_name) if publisher.publ_name.startswith(letter) else None)
    # publs = [publisher.publ_name for publisher in publishers]
    # print(set(publs)-set(publets))
    
    # publs = Publisher.query.all()
    # publishers = [publ.publ_name for publ in publs]
    # publishers_by_letter = db.session.query(Publisher).order_by(func.lower(Publisher.publ_name)).all()
    # publs_by_letter = [publ.publ_name for publ in publishers_by_letter]
    # print(len(publs), len(publishers), len(publs_by_letter))
    # print(set(publishers)-set(publs_by_letter))
    
    # auths=Author.query.all()
    # authors = [author.fullname for author in auths]
    # books = Book.query.all()
    # book_auths=[book.author for book in books]
    # print(set(authors)-set(book_auths))
    
    # # db.create_all()
    
    # from sqlalchemy.dialects import postgresql
    # from sqlalchemy.sql import select
    # # q = select(Book.title).where(Book.title.icontains(title_returned))
    # query =q.compile(dialect=postgresql.dialect())
    # print(query)
    # print(query.params)
                
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
    
    return redirect(url_for('main.home', flag='publishers_list'))

@maintenance_bp.route('/vacuum_analyze')
def vacuum_anlz():
    vacuum_analyze()
    return redirect(url_for('main.home', flag='authors_list'))
    
@maintenance_bp.route('/vacuum_full')
def vacuum_fl():
    vacuum_full()
    return redirect(url_for('main.home', flag='publishers_list'))

@maintenance_bp.route('/vacuum')
def vacm():
    vacuum()
    return redirect(url_for('main.home', flag='books_list'))

