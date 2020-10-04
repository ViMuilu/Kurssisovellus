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
    # gets user id maybe own method?
    name = session["username"]
    
    rsuser = db.session.execute("SELECT id FROM users WHERE username=:name",{"name":name })
    
    userId =""
    for row in rsuser.fetchall():
        userId = row[0]


   # yksi sql lause?
    rsuc = db.session.execute("SELECT id_course FROM userCourses WHERE id_user=:userId",{"userId":userId})

    userCourses =[]
    for row in rsuc.fetchall():  
        rsc = db.session.execute("SELECT name FROM courses WHERE id=:courseId",{"courseId":row[0]})
        
        for row in rsc.fetchall():
            userCourses += [row[0]]
    


    
    rsT = db.session.execute("SELECT name FROM courses WHERE id_teacher=:teacherId",{"teacherId":userId})
    teacherCourses =[]
    for row in rsT.fetchall():
        teacherCourses += [row] 
    
    return render_template("menu.html", courses = courses, userCourses = userCourses, teacherCourses = teacherCourses)   

@app.route("/logout")
def logout():
    del session["username"]
    del session["accountType"]
    return redirect("/")
    
@app.route("/NewAccount")
def newAccountForm():
    return render_template("NewAccountForm.html")

@app.route("/CreateANew",methods=["POST"])
def CreateANew():
    session["userExists"] = False  
    username = request.form["username"]
    password = request.form["password"]
    type1 = request.form["type"]
    hash_value = generate_password_hash(password)

    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   
    if user == None:       
        sql = "INSERT INTO users (username,password,type) VALUES (:username,:password,:type)"
        db.session.execute(sql, {"username":username,"password":hash_value,"type":type1})
        db.session.commit()
        return redirect("/")
    else:

        session["userExists"] = True  
        return redirect("/NewAccount")

    

@app.route("/courseInfo",methods=["POST"])
def courseInfo():
    
    name = request.form["name"];
    session["courseName"] = name

    rs = db.session.execute("SELECT username FROM users JOIN courses ON users.id=courses.id_teacher WHERE courses.name=:name",{"name":name})
    teacher = rs.fetchone()[0]
    session["teacher"] = teacher
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
    teach = request.form["teach"]

    rs1 = db.session.execute("SELECT id FROM users WHERE username=:name",{"name":teach })
    t = rs1.fetchone()
    teacherId = t[0]
    
    sql = "INSERT INTO courses (name,description,id_teacher) VALUES (:name,:description,:idTeacher)"
    db.session.execute(sql, {"name":name,"description":description,"idTeacher":teacherId})
    db.session.commit()
    return redirect("/loggedIn")

@app.route("/exit",methods=["POST"])
def exit():
    return redirect("/loggedIn")

@app.route("/joinCourse",methods=["POST"])
def joinCourse():

    courseName = request.form["courseName"]
    username = request.form["username"]
    # Muunna yhdeksi sql kyselyksi
    rs = db.session.execute("SELECT id FROM courses WHERE name=:name",{"name":courseName})
    
    courseId=""
    for row in rs.fetchall():
        courseId = row[0]

    rsuser = db.session.execute("SELECT id FROM users WHERE username=:name",{"name":username})
    
    userId =""
    for row in rsuser.fetchall():
        userId = row[0]


    sql = "SELECT id_user FROM userCourses WHERE id_course=:id_course"
    result = db.session.execute(sql, {"id_course":courseId})
    

    check=False
    for row in result.fetchall():
        if row[0]==userId:
            check = True


    if check==True:
        return redirect("/loggedIn")

    else:
        sql = "INSERT INTO userCourses (id_user,id_course)  VALUES (:id_user,:id_courses)"
        db.session.execute(sql, {"id_user":userId,"id_courses":courseId})
        db.session.commit()  
        return redirect("/loggedIn")

    


