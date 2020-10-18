from db import db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
def login(username, password):

    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   
    
    if user == None:       
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = user[0]

            sql = "SELECT type FROM users WHERE username=:username"
            result = db.session.execute(sql, {"username":username})
            
            type1 = result.fetchone()[0]
            session["accountType"] = type1
            return True
        else:
            
            return False   

def newAccount(username, password, type1):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()   

    if user == None:       
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username,password,type) VALUES (:username,:password,:type)"
        db.session.execute(sql, {"username":username,"password":hash_value,"type":type1})
        db.session.commit()
        return True
    else:
        return False

def getId(user):   
    rsuser = db.session.execute("SELECT id FROM users WHERE username=:name",{"name":user})
    id1 = rsuser.fetchone()[0]
    return id1

def getCourseTeacher(course):
    rs = db.session.execute("SELECT username FROM users JOIN courses ON users.id=courses.id_teacher WHERE courses.name=:name",{"name":course})
    teacher = rs.fetchone()[0]
    return teacher
def getName(idx):
    rs = db.session.execute("SELECT username FROM users  WHERE id=:id",{"id":idx})
    user = rs.fetchone()[0]
    return user
