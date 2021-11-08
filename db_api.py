import pymysql as sql

configs = []

with open("configs.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  # 去掉列表中每一个元素的换行符
        configs.append(line)

CREATE_DB = 'create database if not exists database_lab1'
# 各表初始化语句
CREATE_STUDENT = """
create table  if not exists student
(registno numeric(6,0),
stu_name varchar(20),
primary key (registno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""


def insert_student(registno, stu_name):
    return 'replace into student(registno,stu_name) values (%d,"%s")' % (registno, stu_name)


def get_student(registno):
    return 'select * from student where registno=%d' % (registno)


CREATE_KD = """
create table  if not exists kd
(kdno numeric (4,0),
kd_name varchar (20),
primary key (kdno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""


def insert_kd(kdno, kd_name):
    return 'replace into kd(kdno,kd_name) values (%d,"%s")' % (kdno, kd_name)


def get_kd(kdno):
    return 'select * from kd where kdno=%d' % (kdno)


CREATE_EXAM = """
create table  if not exists exam
(kdno numeric (4,0),
kcno numeric (4,0),
ccno numeric (4,0),
exptime timestamp ,
papername varchar (20),
primary key (kdno,kcno,ccno),
foreign key (kdno) references kd(kdno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""


def get_exam(kdno, kcno, ccno):
    return 'select * from exam where kdno=%d and kcno=%d and ccno=%d' % (kdno, kcno, ccno)


def insert_exam(kdno, kcno, ccno, exptime, papername):
    return 'replace into exam(kdno,kcno,ccno,exptime,papername)' \
           'values(%d,%d,%d,"%s","%s")' % (kdno, kcno, ccno, exptime, papername)


CREATE_EXAM_TAKES = """
create table if not exists exam_takes
(registno numeric (6,0),
seat numeric (3,0),
kdno numeric (4,0),
kcno numeric (4,0),
ccno numeric (4,0),
primary key (registno,kdno,kcno,ccno),
foreign key (registno) references student(registno),
foreign key (kdno,kcno,ccno) references exam(kdno,kcno,ccno)
)ENGINE=innodb DEFAULT CHARSET=utf8;
"""


def insert_exam_takes(registno, seat, kdno, kcno, ccno):
    return 'insert into exam_takes(registno,seat,kdno,kcno,ccno)' \
           'values (%d,%d,%d,%d,%d)' % (registno, seat, kdno, kcno, ccno)


def get_exam_takes(registno, kdno, kcno, ccno):
    return 'select * from exam_takes where registno=%d and kdno=%d and kcno=%d and ccno=%d' % (registno, kdno, kcno, ccno)


def get_db():
    try:
        db = sql.connect(host=configs[0],
                         user=configs[1],
                         password=configs[2])
        cursor = db.cursor()
        cursor.execute(CREATE_DB)
        cursor.close()
        db.close()
        return sql.connect(host=configs[0],
                           user=configs[1],
                           password=configs[2],
                           database=configs[3])
    except:
        print("""数据库连接失败,请检查configs.txt
        4行分别表示主机地址,mysql用户名,mysql密码,mysql中指定database""")
        exit(0)


def init_tables():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(CREATE_STUDENT)
        cursor.execute(CREATE_KD)
        cursor.execute(CREATE_EXAM)
        cursor.execute(CREATE_EXAM_TAKES)
        db.commit()
    except:
        db.rollback()
        cursor.close()
        db.close()
        print("""建表出错,请检查init_tables函数""")
        exit(0)
    cursor.close()
    db.close()


if __name__ == '__main__':
    print(configs)
    init_tables()
