import os.path
from sqlite3 import connect

from flask import Flask, render_template, request, redirect, url_for

from Classes import User, Article

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.sqlite3")
db = connect(db_path, check_same_thread=False)
cursor = db.cursor()
username = None
user = User()


@app.route('/')
def index():
    global username, user
    if user.id == None:
        return render_template("main.html", username="You is not logged", logged=False)
    else:
        return render_template("main.html", username=username, logged=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    global username, user
    if request.method == 'POST':
        usernameS = request.form.get('username')
        password = request.form.get('password')
        user = User()
        user.login(database=db, login=usernameS, password=password, cursor=cursor)
        username = user.firstname + " " + user.lastname
        return redirect(url_for('index', username=username))
    if user.id == None:
        return render_template("login.html", logged=False, urlReg=url_for('register'))
    else:
        return render_template("login.html", logged=True, urlReg=url_for('register'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    global username, user
    if request.method == 'POST':
        usernameS = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')


        user.register(database=db, login=usernameS, password=password, firstname=firstname, lastname=lastname, cursor=cursor)
        username = user.firstname, user.lastname
        return redirect(url_for('index'))
    if user.id == None:
        return render_template("register.html", logged=False, urlLogin=url_for('login'))
    else:
        return render_template("register.html", logged=True, urlLogin=url_for('login'))

@app.route('/create', methods=['POST', 'GET'])
def create():
    global username, user
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        article = Article()
        article.newArticle(name=name, desc=desc, database=db, cursor=cursor, user=user)

        return redirect(url_for('index', username=username))
    return render_template('createArticle.html', username="You is not logged")

@app.route('/listArticles')
def listArticles():
    global username, user
    cursor.execute("SELECT * from articles")
    dict = cursor.fetchall()
    if user.id == None:
        return render_template("articleList.html", username="You is not logged", dict=dict, logged=False)
    else:
        return render_template("articleList.html", username=username, dict=dict, logged=True)

@app.route('/article')
def article():
    global username, user
    art = Article()
    art.fetchById(id=request.args.get('id'), database=db, cursor=cursor)
    if user.firstname == None:
        return render_template("article.html", ArticleName=art.title, ArticleDesc=art.desc, id=art.id, username="You is not logged", logged=False)
    else:
        return render_template("article.html",ArticleName=art.title, ArticleDesc=art.desc, id=art.id, username=username, logged=True)

@app.route('/cmd')
def cmd():
    global user, username
    cmd = request.args.get('cmd')
    if (cmd == "acceptArticle"):
        artID = request.args.get('articleid')
        art = Article()
        art.fetchById(artID, db, cursor)
        art.accept(db, cursor)
        return redirect(url_for('index'))
    elif (cmd == "rejectArticle"):
        artID = request.args.get('articleid')
        art = Article()
        art.fetchById(artID, db, cursor)
        art.reject(db, cursor)
        return redirect(url_for('index'))
    elif (cmd == "articlePage"):       
        artID = request.args.get('id')
        art = Article()
        art.fetchById(artID, db, cursor)
        rebool = False
        print (type(user.GetArtAcRePern(db, cursor, user)))
        print (user.GetArtAcRePern(db, cursor, user))
        if user.GetArtAcRePern(db, cursor, user) == (1,):
            rebool = True
        else:
            rebool = False
        print (type(rebool))
        print (rebool)
        if art.getStatus(db, cursor) == 1 or art.getStatus(db, cursor) == -1:
            rebool = False
        return render_template('article.html', ArticleName = art.title, ArticleDesc = art.desc, id = artID, ArticleAcRePerm=rebool, username=username, logged=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
