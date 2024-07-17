from flask import Flask
import os
from dotenv import load_dotenv
from library.extensions import db, migrate
from library.routes import main_bp

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = os.getenv('DATABASE_URL')
APP_SECR_KEY = os.getenv('APP_SECR_KEY')

def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = APP_SECR_KEY
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_bp)

    return app

