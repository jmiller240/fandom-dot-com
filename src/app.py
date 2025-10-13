

from flask import Flask, render_template, redirect, url_for, session

from src.accounts.views import accounts_bp
from src.core.views import core_bp


# Init app
app = Flask(__name__)
app.secret_key = 'any random string'

# Add blueprints
app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)


@app.route("/")
def index():
    if not 'username' in session:
        return render_template('login.html')
    
    if not 'selected-teams' in session:
        return redirect(url_for('core.team_selection'))

    return redirect(url_for('core.home'))