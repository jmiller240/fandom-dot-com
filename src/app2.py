

from flask import Flask, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# from src.database import USERS

from src.accounts.views import accounts_bp
from src.core.views import core_bp


## Init app ##
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fandom_db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'any random string'


# Add blueprints
app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)


## Init Login Manager ##
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


## SQLAlchemy ##
db = SQLAlchemy(app)

from .models import Account

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    return Account.query.filter(Account.id == user_id).first()
    # user_id = int(user_id) 
    # return USERS.get(user_id)
    # return Users.query.get(int(user_id))


@app.route("/")
def index():
    if not 'username' in session:
        return redirect(url_for('accounts.login'))
    
    if not 'selected-teams' in session:
        return redirect(url_for('core.team_selection'))

    return redirect(url_for('core.home'))