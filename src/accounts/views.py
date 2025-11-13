'''
Jack Miller
Nov 2025
'''


from flask import flash, Blueprint, request, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user   
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import Account
from src.extensions import db
from src.forms import RegistrationForm, LoginForm


''' Blueprint '''

accounts_bp = Blueprint('accounts', __name__)


''' Routes'''

@accounts_bp.route("/register", methods=['GET', 'POST'])
def register():
    
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        name = form.name.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            print(f'Passwords don\'t match!')
            flash(f'Passwords don\'t match!', 'error')
            return render_template('register.html', form=form)
        
        if Account.query.filter_by(username=username).first():
            print(f'Username already taken')
            flash(message=f'Username already taken.', category='error')
            return render_template('register.html', form=form)

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Account(username=username, name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        print(f'Successfully registered.')
        flash(f'Successfully registered.', category='success')
        return redirect(url_for("core.team_selection"))

    return render_template('register.html', form=form)

@accounts_bp.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        
        user: Account = Account.query.filter_by(username=username).first()
        print(user)

        if user and check_password_hash(user.password, password):       # and check_password_hash(user.password, password):
            print('User:', user)

            login_user(user)
            session['username'] = username
            flash("Successfully logged in.", category='success')

            return redirect(url_for('core.home'))

        else:
            print('wrong password')
            flash('Invalid username or password', category='error')
            return render_template("login.html", form=form)
    
    return render_template('login.html', form=form)

    
@accounts_bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("Successfully logged out.", category='success')

    return redirect(url_for('core.index'))
