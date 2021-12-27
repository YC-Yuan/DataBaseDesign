DROP TABLE IF EXISTS offer;
DROP TABLE IF EXISTS participate;
DROP TABLE IF EXISTS take;
DROP TABLE IF EXISTS log;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS leader;
DROP TABLE IF EXISTS instructor;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS department;

CREATE TABLE department
(
    dept_id INT         NOT NULL AUTO_INCREMENT,
    name    VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (dept_id)
);

CREATE TABLE user
(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(40) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE admin
(
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY (username),
    FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE employee
(
    user_id   CHAR(11)     NOT NULL,
    username  VARCHAR(20)  NOT NULL,
    name      VARCHAR(20)  NOT NULL,
    gender    VARCHAR(10)  NOT NULL CHECK (gender IN ("男", "女")),
    age       INTEGER      NOT NULL CHECK (age >= 0),
    hire_date DATE         NOT NULL,
    city      VARCHAR(255) NOT NULL,
    telephone CHAR(11)     NOT NULL,
    email     VARCHAR(255) NOT NULL,
    dept_name VARCHAR(20),
    PRIMARY KEY (user_id),
    FOREIGN KEY (username) REFERENCES user (username) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dept_name) REFERENCES department (name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE staff
(
    user_id CHAR(11) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id)
);

CREATE TABLE instructor
(
    user_id     CHAR(11) NOT NULL,
    office_date DATE     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id)
);

CREATE TABLE leader
(
    user_id     CHAR(11) NOT NULL,
    office_date DATE     NOT NULL,
    dept_name VARCHAR(20) UNIQUE,
    FOREIGN KEY (user_id) REFERENCES employee (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (dept_name) REFERENCES department (name) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id)
);

CREATE TABLE course
(
    course_id  CHAR(5)      NOT NULL,
    name       VARCHAR(20)  NOT NULL,
    content    VARCHAR(255) NOT NULL,
    category   VARCHAR(20)  NOT NULL,
    start_time DATE         NOT NULL,
    end_time   DATE         NOT NULL,
    instructor_id    CHAR(11)     NOT NULL,
    PRIMARY KEY (course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE log
(
    log_id    INT          NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    operation VARCHAR(255) NOT NULL,
    date      TIMESTAMP    NOT NULL,
    PRIMARY KEY (log_id),
    FOREIGN KEY (username) REFERENCES user (username) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE take
(
    user_id    CHAR(11) NOT NULL,
    course_id  CHAR(5)  NOT NULL,
    evaluation VARCHAR(20) CHECK (evaluation IS NULL OR evaluation IN ("通过", "未通过")),
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES staff (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE participate
(
    user_id   CHAR(11)  NOT NULL,
    course_id CHAR(5)   NOT NULL,
    time      TIMESTAMP NOT NULL,
    score     INT       NOT NULL CHECK (score >= 0 AND score <= 100),
    PRIMARY KEY (user_id, course_id, time),
    FOREIGN KEY (user_id, course_id) REFERENCES take (user_id, course_id) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE offer
(
    dept_id   INT         NOT NULL,
    course_id CHAR(5)     NOT NULL,
    need   VARCHAR(10) NOT NULL CHECK (need IN ("必修", "选修")
        ),
    PRIMARY KEY (dept_id, course_id),
    FOREIGN KEY (dept_id) REFERENCES department (dept_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE ON UPDATE CASCADE
);