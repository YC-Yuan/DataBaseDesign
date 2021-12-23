# 数据库设计PJ

员工培训管理系统

[学号] 赵书誉

19302010020 袁逸聪

## E-R模型设计

![E-R](./E-R.jpg)

## E-R图转换为关系模式

### 实体集

- 课程信息 course (<u>course_id</u>, name, category, content, time_slot)

- 部门信息 department (<u>dept_id</u>, name)

- 账户信息 user (<u>user_id</u>, username, password)

- 职员信息 employee (<u>user_id</u>, name, gender, age, hiredate, city, telephone, email)

- 教师信息 instructor (<u>instructor_id</u>, instructor_name, instructor_class, dept_name)

- 经理信息 leader (<u>leader_id</u>)

- 普通员工信息 staff (<u>staff_id</u>)

- 管理员信息 admin (<u>admin_id</u>)

- 日志信息 log (<u>log_id</u>, operation, date)

  

### 关系集

- 职员 & 部门：属于 belong (<u>user_id</u>, <u>dept_id</u>)
- 普通员工 & 课程：培训 take (<u>staff_id</u>, <u>course_id</u>)
- 教师 & 开课：教授 teach (<u>instructor_id</u>, <u>course_id</u>, date)
- 经理 & 部门：领导 lead (<u>leader_id</u>, <u>dept_id</u>)
- 用户 & 日志：痕迹 leave (<u>user_id</u>, <u>log_id</u>)



### 关系模式对应建表sql

+ course：课程信息

```sqlite
CREATE TABLE "course" (
  "course_id" TEXT(255) NOT NULL,
  "name" TEXT(255) NOT NULL,
  "content" TEXT(255) NOT NULL,
  "category" TEXT(255) NOT NULL,
  "time_slot" TEXT(255) NOT NULL,
  PRIMARY KEY ("course_id"),
  FOREIGN KEY ("category") REFERENCES "department" ("name") ON DELETE CASCADE ON UPDATE CASCADE,
);
```

- department：部门信息

```sqlite
CREATE TABLE "department" (
  "dept_id" TEXT(255) NOT NULL,
  "name" TEXT(255) NOT NULL UNIQUE,
  PRIMARY KEY ("dept_id")
);
```

- user：用户信息

```sqlite
CREATE TABLE "user" (
  "user_id" TEXT(255) NOT NULL,
  "username" TEXT(255) UNIQUE NOT NULL,
  "password" TEXT(255) NOT NULL,
  PRIMARY KEY ("user_id")
);
```

- employee：职员信息

```sqlite
CREATE TABLE "employee" (
  "user_id" TEXT(255) NOT NULL,
  "name" TEXT(255) NOT NULL,
  "gender" TEXT(255) NOT NULL CHECK (gender IN ("Male", "Female")),
  "age" INTEGER(3) NOT NULL,
  "hiredate" TEXT(255) NOT NULL,
  "city" TEXT(255) NOT NULL,
  "telephone" TEXT(255) NOT NULL,
  "email" TEXT(255) NOT NULL,
  PRIMARY KEY ("user_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- admin：管理员信息

```sqlite
CREATE TABLE "admin" (
  "admin_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("admin_id"),
  FOREIGN KEY ("admin_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- staff：普通员工信息

```sqlite
CREATE TABLE "staff" (
  "staff_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("staff_id"),
  FOREIGN KEY ("staff_id") REFERENCES "employee" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- leader：

```sqlite
CREATE TABLE "leader" (
  "leader_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("leader_id"),
  FOREIGN KEY ("leader_id") REFERENCES "employee" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- instructor：

```sqlite
CREATE TABLE "instructor" (
  "instructor_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("instructor_id"),
  FOREIGN KEY ("instructor_id") REFERENCES "employee" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- log：

```sqlite
CREATE TABLE "log" (
  "log_id" TEXT(255) NOT NULL,
  "operation" TEXT(255) NOT NULL,
  "date" TEXT(255) NOT NULL,
  PRIMARY KEY ("log_id")
);
```

- belong

```sqlite
CREATE TABLE "belong" (
  "user_id" TEXT(255) NOT NULL,
  "dept_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("user_id", "dept_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("dept_id") REFERENCES "department" ("dept_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- take

```sqlite
CREATE TABLE "take" (
  "staff_id" TEXT(255) NOT NULL,
  "course_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("staff_id", "course_id"),
  FOREIGN KEY ("staff_id") REFERENCES "staff" ("staff_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("course_id") REFERENCES "course" ("course_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- teach

```sqlite
CREATE TABLE "teach" (
  "instructor_id" TEXT(255) NOT NULL,
  "course_id" TEXT(255) NOT NULL,
  "date" TEXT(255) NOT NULL,
  PRIMARY KEY ("instructor_id", "course_id"),
  FOREIGN KEY ("instructor_id") REFERENCES "instructor" ("instructor_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("course_id") REFERENCES "course" ("course_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- lead

```sqlite
CREATE TABLE "lead" (
  "leader_id" TEXT(255) NOT NULL,
  "dept_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("leader_id", "dept_id"),
  FOREIGN KEY ("leader_id") REFERENCES "leader" ("leader_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("dept_id") REFERENCES "department" ("dept_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```

- leave

```sqlite
CREATE TABLE "leave" (
  "user_id" TEXT(255) NOT NULL,
  "log_id" TEXT(255) NOT NULL,
  PRIMARY KEY ("user_id", "log_id"),
  FOREIGN KEY ("user_id") REFERENCES "user" ("user_id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("log_id") REFERENCES "log" ("log_id") ON DELETE CASCADE ON UPDATE CASCADE
);
```



## 函数依赖与范式分析



## 约束条件分析与实现



## 使用指南



### Django



### API说明
