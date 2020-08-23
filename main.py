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
users = []


@app.route('/')
def index():
    global username, user
    if getUser().id is None:
        return render_template("main.html", username="You is not logged", logged=False, Alscript=request.args.get('Alscript'), alscriptuse=request.args.get('AlscriptUse'))
    else:
        return render_template("main.html", username=getUser().firstname + " " + getUser().lastname, logged=True)


@app.route('/login', methods=['POST', 'GET'])
def login():
    global username, users
    if request.method == 'POST':
        usernameS = request.form.get('username')
        password = request.form.get('password')
        user = User()
        user.login(database=db, login=usernameS, password=password, cursor=cursor)
        addUser(user)
        if getUser().id is not None:
            return redirect(url_for('index', username=getUser().firstname + " " + getUser().lastname))
        else:
            return redirect(url_for('index', logged=False, alscriptuse=True))
    if getUser().id is None:
        return render_template("login.html", logged=False, urlReg=url_for('register'))
    else:
        return render_template("login.html", logged=True, urlReg=url_for('register'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    global username, users
    if request.method == 'POST':
        usernameS = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        user = User()
        user.register(database=db, login=usernameS, password=password, firstname=firstname, lastname=lastname,
                      cursor=cursor)
        username = getUser().firstname, getUser().lastname
        return redirect(url_for('index'))
    if getUser().id is None:
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
        article.newArticle(name=name, desc=desc, database=db, cursor=cursor, user=getUser())

        return redirect(url_for('index', username=username))
    return render_template('createArticle.html', username="You is not logged")


@app.route('/listArticles')
def listArticles():
    global username, users
    cursor.execute("SELECT * from articles")
    dict = cursor.fetchall()
    if getUser().id == None:
        return render_template("articleList.html", username="You is not logged", dict=dict, logged=False)
    else:
        return render_template("articleList.html", username=getUser().firstname + " " + getUser().lastname, dict=dict, logged=True)


@app.route('/article')
def article():
    global username, users
    art = Article()
    art.fetchById(id=request.args.get('id'), database=db, cursor=cursor)
    if getUser().firstname == None:
        return render_template("article.html", ArticleName=art.title, ArticleDesc=art.desc, id=art.id,
                               username="You is not logged", logged=False)
    else:
        return render_template("article.html", ArticleName=art.title, ArticleDesc=art.desc, id=art.id,
                               username=getUser().firstname + " " + getUser().lastname, logged=True)


@app.route('/cmd')
def cmd():
    global users, username
    cmd = request.args.get('cmd')
    if cmd == "acceptArticle":
        artID = request.args.get('articleid')
        art = Article()
        art.fetchById(artID, db, cursor)
        art.accept(db, cursor)
        return redirect(url_for('index'))
    elif cmd == "rejectArticle":
        artID = request.args.get('articleid')
        art = Article()
        art.fetchById(artID, db, cursor)
        art.reject(db, cursor)
        return redirect(url_for('index'))
    elif cmd == "articlePage":
        artID = request.args.get('id')
        art = Article()
        art.fetchById(artID, db, cursor)
        rebool = False
        print(type(getUser().GetArtAcRePern(db, cursor, getUser())))
        print(getUser().GetArtAcRePern(db, cursor, getUser()))
        if getUser().GetArtAcRePern(db, cursor, getUser()) == (1,):
            rebool = True
        else:
            rebool = False
        print(type(rebool))
        print(rebool)
        if art.getStatus(db, cursor) == 1 or art.getStatus(db, cursor) == -1:
            rebool = False
        return render_template('article.html', ArticleName=art.title, ArticleDesc=art.desc, id=artID,
                               ArticleAcRePerm=rebool, username=getUser().firstname + " " + getUser().lastname, logged=True)

def getUser():
    global users
    user = User()
    for i in range(0, len(users)):
        if users[i][0] == request.remote_addr:
            return users[i][1]
    return user

def addUser(user):
    global users
    for i in range(0, len(users)):
        if users[i][0] == request.remote_addr:
            del users[i]

    users.append([request.remote_addr, user])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
