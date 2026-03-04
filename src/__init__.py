'''
Jack Miller
November 2025

Module home, provides function that creates application.
'''

# Python
import os
from dotenv import load_dotenv

from flask import Flask

# Application
from src.extensions import db, login_manager
from src.models import Account
from src.accounts.views import accounts_bp
from src.core.views import core_bp


## Main func ##

def create_app():

    # Get DB Url
    env = os.getenv('ENVIRONMENT')
    if env == 'DEV':
        database_url = os.getenv('DATABASE_URL_DEV')
    else:
        database_url = os.getenv('DATABASE_URL_PROD')

    ## App ##
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = 'any random string'

    # Add blueprints
    app.register_blueprint(accounts_bp)
    app.register_blueprint(core_bp)

    # Init Login Manager
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
        user_id = int(user_id)
        return Account.query.filter(Account.id == user_id).first()

    # SQLAlchemy
    db.init_app(app)

    # Inject app with information
    @app.context_processor
    def inject_global_vars():
        return {
            'leagues': ['NFL', 'NBA', 'MLB', 'CFB', 'NCAAM', 'PREM']
        }

    return app