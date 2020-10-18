CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, type INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, name TEXT, description  TEXT, id_teacher INT,FOREIGN KEY (id_teacher) REFERENCES users(id)ON DELETE CASCADE);
CREATE TABLE userCourses (id_user INTEGER,id_course INTEGER,FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (id_course) REFERENCES courses(id)ON DELETE CASCADE);
CREATE TABLE Taskdata (id SERIAL PRIMARY KEY, id_course int, question TEXT, answer TEXT, correctAnswer TEXT, FOREIGN KEY (id_course) REFERENCES courses(id)ON DELETE CASCADE);
CREATE TABLE Taskprogression (id_task INT, id_user INT, grade BOOLEAN,  FOREIGN KEY (id_user) REFERENCES users(id)ON DELETE CASCADE,FOREIGN KEY (id_task) REFERENCES TaskData(id)ON DELETE CASCADE);
