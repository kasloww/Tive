from flask import Flask, render_template, request, redirect
import pymysql
import pymysql.cursors
app = Flask(__name__)

conn = pymysql.connect(
    database="kdavidson_",
    user="kdavidson",
    password="231534561",
    host="10.100.33.60",
    cursorclass=pymysql.cursors.DictCursor
)
if __name__ == '__main__':
    app.run()
@app.route('/')
def index():
    return render_template('tive.html.jinja')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO `Users` (`User`, `Password`) VALUES ('{username}', '{password}')")
        cursor.close()
        conn.commit()
    return render_template('tive.signup.jinja')
    
@app.route('/signin', methods=['GET', 'POST'])
def sign():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `Users` WHERE `User` = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        conn.commit()
        if password == user["Password"]:
            return redirect('/feed')
    return render_template('tive.signin.jinja')

@app.route('/feed')
def fed():
    return render_template('tive.feed.jinja')