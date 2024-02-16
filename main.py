from flask import Flask, g, render_template, request, redirect
import flask_login
import pymysql
import pymysql.cursors
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = "top_secret"

login_manager =flask_login.LoginManager()

login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = True
    is_active = True

    def __init__(self, id, username, password):
        self.username = username
        self.id = id
        self.password = password

    def get_id(self):

        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * from `Users` WHERE `ID` = " + str(user_id))
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

    if result is None:

        return None
    
    return User(result['ID'], result['User'], result)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="kdavidson",
        password="231534561",
        database="kdavidson_",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    
    return render_template('tive.html.jinja')

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `Users` (`User`, `Password`) VALUES ('{username}', '{password}')")
        cursor.close()
        get_db().commit()
    return render_template('tive.signup.jinja')
    
@app.route('/signin', methods=['GET', 'POST'])
def sign():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `Users` WHERE `User` = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        get_db().commit()

        if password == user['Password']:
            user = load_user(user['ID'])

            flask_login.login_user(user)

            return redirect('/feed')
        
    return render_template('tive.signin.jinja')

@app.route('/feed')
@flask_login.login_required
def fed():
    cursor = get_db().cursor()

    cursor.execute("SELECT `Description`, `User_ID`, `Timestamp` FROM `Posts`")

    results = cursor.fetchall()
    
    return render_template('tive.feed.jinja', posted=results)

@app.route('/post', methods=["POST"])
@flask_login.login_required
def posted():
    posting = request.form['post_made']

    cursor = get_db().cursor()

    cursor.execute(f"INSERT INTO `Posts`(`Description`, `User_ID`) VALUES ('{posting}')")