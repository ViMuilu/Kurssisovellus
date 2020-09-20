from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def loginFrom():
    return render_template("loginForm.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   
    if user == None:       
        return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username

            sql = "SELECT type FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            
            type1 = result.fetchone()[0]
            session["accountType"] = type1
            return redirect("/loggedIn")
        else:
            
            return redirect("/")
            
@app.route("/loggedIn")
def loggedIn():
    rs = db.session.execute("SELECT name FROM courses")
    courses = rs.fetchall()

    return render_template("menu.html", courses = courses, )   

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/NewAccount")
def newAccountForm():
    return render_template("NewAccountForm.html")

@app.route("/CreateANew",methods=["POST"])
def CreateANew():
    username = request.form["username"]
    password = request.form["password"]
    type1 = request.form["type"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password,type) VALUES (:username,:password,:type)"
    db.session.execute(sql, {"username":username,"password":hash_value,"type":type1})
    db.session.commit()
    return redirect("/")

@app.route("/courseInfo",methods=["POST"])
def courseInfo():
    name = request.form["name"];
    rs1 = db.session.execute("SELECT description FROM courses WHERE name=:name",{"name":name })
    desc = rs1.fetchall()
    return render_template("courseInfo.html", desc = desc)

@app.route("/newCourse",methods=["POST"])
def newCourse():
    return render_template("newCourse.html")


@app.route("/course", methods=["POST"])
def course():
    name = request.form["name"]
    description = request.form["desc"]
    sql = "INSERT INTO courses (name,description) VALUES (:name,:description)"
    db.session.execute(sql, {"name":name,"description":description})
    db.session.commit()
    return redirect("/loggedIn")

