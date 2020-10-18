from db import db
from flask import redirect, render_template, request, session
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors


def getId(courseName): 
    rsuser = db.session.execute("SELECT id FROM courses WHERE name=:name",{"name":courseName })
    id1 = rsuser.fetchone()
    return id1

def createCourse(name,description,teacherId):
        if(getId(name) == None):
            sql = "INSERT INTO courses (name,description,id_teacher) SELECT :name,:description,:idTeacher"
            db.session.execute(sql, {"name":name,"description":description,"idTeacher":teacherId})
            db.session.commit()
            return True
        else:
            return False
def getCourses():
    rs = db.session.execute("SELECT name FROM courses")
    courses = rs.fetchall()
    return courses


def addToCourse(userId,courseId):

    sql = "SELECT id_user FROM userCourses WHERE id_course=:id_course"
    result = db.session.execute(sql, {"id_course":courseId[0]})
    check = True
    for row in result.fetchall():
        if row[0]==userId:
            check = False
            
    if(check):
        sql = "INSERT INTO userCourses (id_user,id_course)  VALUES (:id_user,:id_courses)"
        db.session.execute(sql, {"id_user":userId,"id_courses":courseId[0]})
        db.session.commit()  
    
def getCoursesById(userId):

    if(session["accountType"] == 1):
        rsuc = db.session.execute("SELECT name FROM courses JOIN userCourses ON courses.id=userCourses.id_course WHERE userCourses.id_user=:userId",{"userId":userId})
        studentsCourses = rsuc.fetchall()
        return studentsCourses
    elif (session["accountType"] == 2):
            rsT = db.session.execute("SELECT name FROM courses WHERE id_teacher=:teacherId",{"teacherId":userId})
            return rsT.fetchall()

def getCourseDescription(courseName):
    rs1 = db.session.execute("SELECT description FROM courses WHERE name=:name",{"name":courseName})
    desc = rs1.fetchone()[0]
    return desc
    
def deleteCourse(courseName):
    db.session.execute("DELETE FROM courses WHERE name=:name",{"name":courseName})
    db.session.commit()

def editDescription(courseName, description):
    db.session.execute("UPDATE courses SET description=:desc WHERE name=:name",{"desc":description,"name":courseName})
    db.session.commit()

def getCourseStudents(courseId):
    sql = "SELECT id_user FROM userCourses WHERE id_course=:id_course"
    result = db.session.execute(sql, {"id_course":courseId})
    return result.fetchall()