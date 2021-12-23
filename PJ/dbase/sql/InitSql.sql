DROP TABLE IF EXISTS department;
CREATE TABLE department (
  dept_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (dept_id)
);

DROP TABLE IF EXISTS course;
CREATE TABLE course (
  course_id CHAR(5) NOT NULL,
  name VARCHAR(20) NOT NULL,
  content VARCHAR(255) NOT NULL,
  category VARCHAR(20) NOT NULL,
  start_time DATE NOT NULL,
  end_time DATE NOT NULL,
  PRIMARY KEY (course_id)
);

DROP TABLE IF EXISTS user;
CREATE TABLE user (
  username VARCHAR(20) NOT NULL,
  password VARCHAR(40) NOT NULL,
  PRIMARY KEY (username)
);
DROP TABLE IF EXISTS "admin";
CREATE TABLE "admin" (
  "username" VARCHAR(20) NOT NULL,
  PRIMARY KEY (username),
  FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
  user_id CHAR(11) NOT NULL,
  username VARCHAR(20) NOT NULL,
  name VARCHAR(20) NOT NULL,
  gender VARCHAR(10) NOT NULL CHECK (gender IN ("男", "女")),
  age INTEGER NOT NULL,
  hiredate DATE NOT NULL,
  city VARCHAR(255) NOT NULL,
  telephone CHAR(11) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
  user_id CHAR(11) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS instructor;
CREATE TABLE instructor (
  user_id CHAR(11) NOT NULL,
  office_date DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS leader;
CREATE TABLE leader (
  user_id CHAR(11) NOT NULL,
  office_date DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS log;
CREATE TABLE log (
  log_id INT NOT NULL AUTO_INCREMENT,
  operation VARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (log_id)
);

DROP TABLE IF EXISTS belong;
CREATE TABLE belong (
  user_id CHAR(11) NOT NULL,
  dept_id INT NOT NULL,
  PRIMARY KEY (user_id, dept_id),
  FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (dept_id) REFERENCES department (dept_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS take;
CREATE TABLE take (
  user_id CHAR(11) NOT NULL,
  course_id CHAR(5) NOT NULL,
  evaluation VARCHAR(20),
  PRIMARY KEY (user_id, course_id),
  FOREIGN KEY (user_id) REFERENCES staff (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS participate;
CREATE TABLE participate (
  user_id CHAR(11) NOT NULL,
  course_id CHAR(5) NOT NULL,
  time TIMESTAMP NOT NULL,
  score INT NOT NULL CHECK(score >= 0 AND score <= 100),
  PRIMARY KEY (user_id, course_id, time),
  FOREIGN KEY (user_id) REFERENCES staff (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS teach;
CREATE TABLE teach (
  user_id CHAR(11) NOT NULL,
  course_id CHAR(5) NOT NULL,
  PRIMARY KEY (user_id, course_id),
  FOREIGN KEY (user_id) REFERENCES instructor (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS charge;
CREATE TABLE charge (
  user_id CHAR(11) NOT NULL,
  dept_id INT NOT NULL,
  PRIMARY KEY (user_id, dept_id),
  FOREIGN KEY (user_id) REFERENCES leader (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (dept_id) REFERENCES department (dept_id) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS trace;
CREATE TABLE trace (
  username VARCHAR(20) NOT NULL,
  log_id INT NOT NULL,
  PRIMARY KEY (username, log_id),
  FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (log_id) REFERENCES log (log_id) ON DELETE CASCADE ON UPDATE CASCADE
);