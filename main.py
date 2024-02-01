from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('tive.html.jinja')

@app.route('/register')
def reg():
    return render_template('tive.signup.jinja')
if __name__ == '__main__':
    app.run()
@app.route('/Tive/<name>')
def tive(name):
    return 'Welcome to ' + name