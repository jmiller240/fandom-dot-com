from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    print(os.getcwd())
    return render_template('hello.html', name='Gabi')