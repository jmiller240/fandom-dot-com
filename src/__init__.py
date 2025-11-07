

from flask import Flask

from src.extensions import db, login_manager

from src.models import Account

from src.accounts.views import accounts_bp
from src.core.views import core_bp


def create_app():

    ## App ##
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/jack.miller/Documents/Personal/fandom-dot-com/fandom_db3.db"
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

    return app