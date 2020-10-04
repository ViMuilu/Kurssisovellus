CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, type INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, name TEXT, description  TEXT, id_teacher INT,FOREIGN KEY (id_teacher) REFERENCES users(id));
CREATE TABLE userCourses (id_user INTEGER,id_course INTEGER,FOREIGN KEY (id_user) REFERENCES users(id), FOREIGN KEY (id_course) REFERENCES courses(id));
CREATE TABLE Taskdata (id SERIAL PRIMARY KEY, id_course int, question TEXT, button TEXT, FOREIGN KEY (id_course) REFERENCES courses(id));
CREATE TABLE Taskprogression (id_task INT, id_user INT, grade BOOLEAN,  FOREIGN KEY (id_user) REFERENCES users(id),FOREIGN KEY (id_task) REFERENCES TaskData(id));
