from db import db
from flask import redirect, render_template, request, session


def addTask(courseId,question,answer,correctAnswer):
    sql = "INSERT INTO Taskdata (id_course,question,answer,correctAnswer) VALUES (:id_course,:question,:answer,:correctAnswer) "
    db.session.execute(sql, {"id_course":courseId[0],"question":question,"answer":answer,"correctAnswer":correctAnswer})
    db.session.commit()
 
def addGradeToUserTask(idTask,idUser,result):
    sql = "INSERT INTO Taskprogression (id_task,id_user,grade) SELECT :id_task,:id_user,:grade WHERE NOT EXISTS(SELECT id_task,id_user FROM Taskprogression WHERE id_task=:id_task AND id_user=:id_user) "
    db.session.execute(sql, {"id_task":idTask[0],"id_user":idUser,"grade":result})
    db.session.commit()

def getTaskData(name):
    rs = db.session.execute("SELECT answer, correctAnswer FROM Taskdata WHERE question=:taskName",{"taskName":name})
    answersAll = rs.fetchall()[0]
    return answersAll

def getTasks(courseName):
    rsTasks = db.session.execute("SELECT question FROM Taskdata JOIN courses ON Taskdata.id_course = courses.id WHERE courses.name=:name",{"name":courseName})
    tasks = rsTasks.fetchall()
    return tasks
def getTaskId(name):
    rs = db.session.execute("SELECT id FROM Taskdata WHERE question=:taskName",{"taskName":name})
    idT = rs.fetchone()
    return idT

def getAnswers(task,idUser):
    rsTasks = db.session.execute("SELECT grade FROM Taskprogression JOIN Taskdata ON Taskdata.id = Taskprogression.id_task WHERE Taskdata.question=:name AND Taskprogression.id_user=:userId",{"name":task,"userId": idUser})
    answer = rsTasks.fetchone()
    return answer

def deleteTask(taskName):
    db.session.execute("DELETE FROM Taskdata WHERE question=:name",{"name":taskName})
    db.session.commit() 