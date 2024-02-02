from flask import Flask, render_template, request
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
if __name__ == '__main__':
    app.run()