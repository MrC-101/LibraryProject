from library.extensions import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, nullable=True)
    first_publish = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, nullable=True)