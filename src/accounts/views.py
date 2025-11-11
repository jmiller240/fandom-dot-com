
from flask import flash, Blueprint, request, redirect, render_template, url_for, session
from flask_login import login_required, login_user, logout_user   
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import Account, Team
from src.extensions import db
from src.forms import RegistrationForm, LoginForm

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route("/register", methods=['GET', 'POST'])
def register():
    # if request.method == 'GET':
    #     return render_template('register.html')
    
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data #request.form.get("username")
        name = form.name.data #request.form.get("name")
        password = form.password.data #request.form.get("password")
        confirm_password = form.confirm_password.data #request.form.get("confirm-password")

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
    # if request.method == 'GET':
    #     return render_template('login.html')
    # else:

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data #request.form.get("username")
        password = form.password.data #request.form.get("password")
        
        user: Account = Account.query.filter_by(username=username).first()
        print(user)

        if user and check_password_hash(user.password, password):       # and check_password_hash(user.password, password):
            print('User:', user)

            login_user(user)
            session['username'] = username
            flash("Successfully logged in.", category='success')

            # user_teams: list[Team] = user.teams
            # if user_teams:

            #     # Store teams in session
            #     teams_obj = []
            #     for team in user_teams:
            #         d = {
            #             'appID': team.appID,
            #             'id': team.id,
            #             'name': team.name,
            #             'league': team.league,
            #             'logoURL': team.logoURL
            #         }
            #         teams_obj.append(d)

            #     session['selected-teams'] = teams_obj

            # next_page = request.args.get('next')
            # if next_page:
            #     return redirect(next_page or url_for('accounts.login'))
            # if user.teams:
            return redirect(url_for('core.home'))

            # else:        
            #     return redirect(url_for('core.team_selection', _method='GET'))

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
