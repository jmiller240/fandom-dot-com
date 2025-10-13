
from flask import Blueprint, request, redirect, url_for, session



accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('core.team_selection', _method='GET'))

@accounts_bp.route("/logout")
def logout():
    session.clear()

    return redirect(url_for('index'))
