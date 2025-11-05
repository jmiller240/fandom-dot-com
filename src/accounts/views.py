
from flask import flash, Blueprint, request, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from src.database import USERS, User



accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        
        user: User = None
        for i, user_obj in USERS.items():
            if user_obj.username == username:
                user = user_obj

        if user and user.password == password:       # and check_password_hash(user.password, password):
            login_user(user)
            session['username'] = username
            return redirect(url_for('core.team_selection', _method='GET'))

        else:
            flash('Invalid username or password')
            return render_template("login.html")

    
@accounts_bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()

    return redirect(url_for('index'))
