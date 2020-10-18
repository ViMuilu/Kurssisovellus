from app import app
import users
import courses
import tasks
from flask import redirect, render_template, request, session

@app.route("/")
def loginForm():
    session.clear()
    return render_template("loginForm.html", )
@app.route("/exit")
def exit():
    return redirect("/loggedIn")
    
@app.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "GET":
        session.clear()
        return render_template("loginForm.html",message="")
    if request.method == "POST":
        
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):

            session["username"] = username
            return redirect("/loggedIn")
        else:
            return render_template("loginForm.html",message="Wrong username or password")   

@app.route("/createANew",methods=["GET","POST"])
def createANew():  
    if request.method == "GET":
        session["userExists"] = False
        return render_template("NewAccountForm.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        type1 = request.form["type"]
        
        if users.newAccount(username,password,type1):
            return redirect("/")
        else:
            session["userExists"] = True
            return render_template("NewAccountForm.html")   
@app.route("/loggedIn")
def loggedIn():
    name = session["username"]
    
    userId = users.getId(name)
    cours=[]
    userCourses =[]
    
    for row in courses.getCourses():
        cours +=row
       
    for row in courses.getCoursesById(userId): 
        userCourses +=row
    session["courses"] = cours
    session["usercourses"] = userCourses
    return render_template("menu.html", courses = cours, userCourses = userCourses, teacherCourses = userCourses)


@app.route("/courseInfo",methods=["GET","POST"])
def courseInfo():
    if request.method == "GET":
        return render_template("courseInfo.html")
    if request.method == "POST":    
        courseName = request.form["name"];

        session["teacher"] = users.getCourseTeacher(courseName)
        session["courseName"] = courseName
    
        usersCourse = courses.getCoursesById(users.getId(session["username"]))
        session["notOnCourse"] = True
        for course in usersCourse:
            if course[0] == courseName:          
                session["notOnCourse"] = False

        t = tasks.getTasks(courseName)
        tas =[]
        ta = []
        for task in t: 
            
            answer = tasks.getAnswers(task[0],users.getId(session["username"]))
            tas.append(task[0])
            
            if answer == None:
                ta.append(task[0] + ", Not done" )
            elif answer[0] == True:
                ta.append(task[0] + ", Correct answer")
            else:
                ta.append(task[0] + ", Wrong answer")    
            
        session["desc"] = courses.getCourseDescription(courseName)
        session["task"] = tas
        session["taskAnswers"] = ta
        return render_template("courseInfo.html")


@app.route("/course", methods=["GET","POST"])
def course():

    if request.method == "GET":
        session["error"] = ""
        return render_template("newCourse.html")


    if request.method == "POST":
        name = request.form["name"]
        description = request.form["desc"]
        teach = request.form["teach"]

        idTeach = users.getId(teach)

        if courses.createCourse(name,description,idTeach):
            return redirect("/loggedIn")
        else:
            session["error"] = "Course with this name exists"
            return render_template("newCourse.html")
        


@app.route("/joinCourse",methods=["POST"])
def joinCourse():

    courseName = request.form["courseName"]
    username = request.form["username"] 
    courseId= courses.getId(courseName)
    userId = users.getId(username)    
    courses.addToCourse(userId,courseId)
    return redirect("/loggedIn")

@app.route("/createTask",methods=["GET","POST"])
def createTask():

    if request.method == "GET":
        return render_template("newTask.html")

    if request.method == "POST":
        question = request.form["question"]
        answer = request.form["btn"]
        correctAnswer = request.form["correctAnswer"]
        course = request.form["course"]

        
        if  not question or not answer  or not correctAnswer:
        
            return render_template("newTask.html")

        courseId = courses.getId(course)
        
        tasks.addTask(courseId, question, answer, correctAnswer)
       
        return redirect("/courseInfo")

@app.route("/task",methods=["POST"])
def task():

    taskName = request.form["name"]

    answersAll = tasks.getTaskData(taskName)

    answers = answersAll[0].split(",")
    correctAnswer = answersAll[-1]

    return render_template("task.html", answers = answers, question = taskName, correctAnswer = correctAnswer)


@app.route("/checkAnswer",methods=["POST"])
def checkAnswer():  

    answer = request.form["answer"]
    cAnswer = request.form["canswer"]
    taskname = request.form["taskname"]

    result = False

    if answer == cAnswer: 
        result = True
        
    
    idTask = tasks.getTaskId(taskname)
    userId = users.getId(session["username"])
    tasks.addGradeToUserTask(idTask,userId,result)
    return redirect("/courseInfo")

@app.route("/editDesc",methods=["GET","POST"])
def editDesc():  
    if request.method == "GET":
        return render_template("editDescription.html")
    if request.method == "POST":
        courses.editDescription(session["courseName"],request.form["description"])
        return redirect("/courseInfo")
    

@app.route("/deleteCourse",methods=["POST"])
def deleteCourse():
    courseName = request.form["courseName"]
    courses.deleteCourse(courseName);
    return redirect("/loggedIn")

@app.route("/deleteTask",methods=["POST"])
def deleteTask():
    taskName = request.form["taskName"]
    tasks.deleteTask(taskName);
    return redirect("/courseInfo")

@app.route("/courseStudentsStats",methods=["POST"])
def getcourseStudentsStats():
    courseId = courses.getId(request.form["courseName"])
    students = courses.getCourseStudents(courseId[0])
    ta = tasks.getTasks(request.form["courseName"])
    studentsAndTasks =[]
    x = 0
    doneTasks = 0
    for student in students:
        
        t = 0
        for task in ta:
            if(tasks.getAnswers(task[0],student[0]) != None):
                if(tasks.getAnswers(task[0],student[0])[0] == True):
                    doneTasks +=1
            t+=1
            

        studentsAndTasks.append(users.getName(student[0]) + " Completed tasks: " + str(doneTasks) + "/" + str(t))
    
    return render_template("courseStats.html", studentsAndTasks = studentsAndTasks)

@app.route("/leaveCourse",methods=["POST"])
def leaveCourses():
    courseId = courses.getId(request.form["name"])
    userId = users.getId(session["username"])
    courses.leaveCourse(userId,courseId[0])
    return redirect("/loggedIn")