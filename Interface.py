from flask import Flask,flash, render_template, url_for, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from Source import *
import sqlite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes= 5)
app.secret_key = "MoviesList"

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)   
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    

    def __init__(self, name, password):
        self.name = name
        self.password = password

@app.route("/search-title", methods=['POST', 'GET'])
def search_title():
    if request.method == "POST":
        title = request.form["search"].title()
        connect= sqlite3.connect(f"Movies_Database/Movies.db")
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM Movies WHERE Title = '{title}';")
        results = cur.fetchall()
        connect.commit()
        connect.close()
        return render_template("rating_down.html", data = results)
    else:
        return redirect(url_for("home"))


@app.route("/rating-up")
def rating_up():
    connect= sqlite3.connect(f"Movies_Database/Movies.db")
    cur = connect.cursor()
    cur.execute("SELECT * FROM Movies GROUP BY Title ORDER By Rating ASC;")
    results = cur.fetchall()
    connect.commit()
    values = [row for row in results]
    connect.close()
    return render_template("rating_up.html", data = values)

@app.route("/rating-down")
def rating_down():
    connect= sqlite3.connect(f"Movies_Database/Movies.db")
    cur = connect.cursor()
    cur.execute("SELECT * FROM Movies GROUP BY Title ORDER By Rating DESC ;")
    results = cur.fetchall()
    connect.commit()
    values = [row for row in results]
    connect.close()
    return render_template("rating_down.html", data = values)

@app.route("/favorite")
def favoriteMovies():
    if "user" in session:
        connect= sqlite3.connect(f"User_Data/{session['user']}.db")
        cur = connect.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Movies'")
        if cur.fetchone() is None:
            # If the Movies table does not exist, redirect to home
            flash("You have not added any favorite movies yet")
            return redirect(url_for('home'))
        
        cur.execute("SELECT * FROM Movies")
        results = cur.fetchall()
        connect.commit()
        values = [row for row in results]
        return render_template("favorite.html", data = values)
    else:
        return render_template("login.html")
    
def delete_from_DB(id):
    connect= sqlite3.connect(f"User_Data/{session['user']}.db")
    cur = connect.cursor()
    cur.execute(f"DELETE From Movies where ID = {id}")
    connect.commit()
    return {"status": "success"}

@app.route("/delete-data", methods = ["POST"])
def delete_data():
    data = request.get_json()
    value = int(data.get('value'))
    result = delete_from_DB(value)
    return jsonify(result)

def check_unique_fav_movie(connect, cur, id):
    cur.execute("SELECT ID FROM Movies")
    results = cur.fetchall()
    connect.commit()
    values = [row[0] for row in results]
    if id not in values:
        return True
    return False

def save_to_database(id):
    connect= sqlite3.connect(f"User_Data/{session['user']}.db")
    cur = connect.cursor()
    values = (data[4][id], data[0][id], data[1][id], data[2][id], data[3][id])

    cur.execute("""CREATE TABLE IF NOT EXISTS Movies (ID, Poster text, Title text, Rating real, Release text)""")
    connect.commit()

    if check_unique_fav_movie(connect,cur, data[4][id]) is True:
        cur.execute("INSERT INTO Movies (ID, Poster, Title, Rating, Release) VALUES (?,?,?,?,?)", values)
        connect.commit()
    else:
        return {'error': 'Invalid value provided'}
    
    favoriteMovies()

    connect.close()
    return {"status": "success"}

@app.route('/save-data', methods=['POST'])
def save_data():
    data = request.get_json()
    value = int(data.get('value'))
    result = save_to_database(value)
    return jsonify(result)

 
@app.route("/home", methods = ["POST", "GET"])
def home():
    if "user" in session:
        return render_template("home.html", data = data)
    else:
        return redirect(url_for("login"))

@app.route("/register" , methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        user = request.form["name"]
        password = request.form["pass"]

        found_user = users.query.filter_by(name = user).first()
        if found_user:
            flash(" ACCOUNT EXISTED, PLEASE LOG IN!")
            session.pop("user",None)
            session.pop("pass", None)
            return redirect(url_for("login"))

        else:
            flash("REGISTER SUCCESFULLY, You can now log in")
            account = users(user, password)
            db.session.add(account)
            db.session.commit()
            return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/" , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        password = request.form["pass"]
    
        session.permanent = True
        session["user"] = user
        
        found_user = users.query.filter_by(name = user).first()

        if found_user:
            
            if password == found_user.password:
                Movies_DB()
                return redirect(url_for("home"))
            else:
                flash("Please type the correct PASSWORD !")
                session.pop("user",None)
                session.pop("pass", None)
                return render_template("login.html")
        
        else:
            flash("You've not register yet")
            session.pop("user",None)
            session.pop("pass", None)
            return render_template("login.html")
        
    
    else:
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("home"))
        
        
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    connect = sqlite3.connect("Movies_Database/Movies.db")
    cursor = connect.cursor()
    cursor.execute("DROP TABLE IF EXISTS Movies;")
    connect.commit()
    connect.close()

    session.pop("user", None)
    session.pop("password",None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
