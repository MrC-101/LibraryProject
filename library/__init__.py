from flask import Flask
import os, pymysql
from dotenv import load_dotenv
from library.extensions import db, migrate
from library.routes.book_routes import book_bp
from library.routes.main_routes import main_bp
from library.routes.author_routes import author_bp
from library.routes.publisher_routes import publisher_bp
from library.routes.maintenance_routes import maintenance_bp
from pathlib import Path

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))
# dotenv_path = Path('/.env')
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL') #postgres
print(DATABASE_URL)
APP_SECR_KEY = os.getenv('APP_SECR_KEY')

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = APP_SECR_KEY
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(author_bp)
    app.register_blueprint(publisher_bp)
    app.register_blueprint(maintenance_bp)
    
    return app
