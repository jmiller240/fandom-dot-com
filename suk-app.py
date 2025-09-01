
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route("/hi", methods=['GET', 'POST'])
def suk_home():
    if request.method == 'GET':
        return render_template('suk/suk-home.html')
    elif request.method == 'POST':
        name = request.form['name']
        if not name:
            return render_template('suk/suk-home.html')
        return redirect(url_for('suk', name=name))

@app.route("/suk/<name>")
def suk(name: str):
    return render_template('suk/suk.html', name=name)

@app.route("/base")
def base():
    return render_template('base.html')