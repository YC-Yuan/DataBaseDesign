import pymysql as sql

CREATE_DB = 'create database if not exists database_lab1'
# 各表初始化语句
CREATE_STUDENT = """
create table  if not exists student
(stu_no numeric(11,0),
stu_name varchar(20),
primary key (stu_no)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""
CREATE_KD = """
create table  if not exists kd
(kdno numeric (4,0),
kd_name varchar (20),
primary key (kdno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""

CREATE_EXAM = """
create table  if not exists exam
(kdno numeric (4,0),
kcno numeric (4,0),
ccno numeric (4,0),
exptime time,
papername varchar (20),
primary key (kdno,kcno,ccno),
foreign key (kdno) references kd(kdno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""

CREATE_EXAM_TAKES = """
create table if not exists exam_takes
(registno numeric (6,0),
seat numeric (3,0),
stu_no numeric(11,0),
kdno numeric (4,0),
kcno numeric (4,0),
ccno numeric (4,0),
primary key (registno),
foreign key (stu_no) references student(stu_no),
foreign key (kdno,kcno,ccno) references exam(kdno,kcno,ccno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""


def get_db():
    db = sql.connect(host='localhost',
                     user='root',
                     password='password')
    cursor = db.cursor()
    cursor.execute(CREATE_DB)
    cursor.close()
    db.close()
    return sql.connect(host='localhost',
                       user='root',
                       password='password',
                       database='database_lab1')


def init_tables():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(CREATE_STUDENT)
    cursor.execute(CREATE_KD)
    cursor.execute(CREATE_EXAM)
    cursor.execute(CREATE_EXAM_TAKES)
    cursor.close()
    db.close()


if __name__ == '__main__':
    init_tables()
