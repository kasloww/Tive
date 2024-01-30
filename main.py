from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tive.jinja')

@app.route('/Tive/<name>')
def tive(name):
    return 'Welcome to ' + name