# DataBaseDesign

19302010020 袁逸聪

Lab使用mysql与python3.9

- mysql  Ver 14.14 Distrib 5.7.33, for Win64 (x86_64)

## 表模型分析

为了尽可能降低数据库的耦合性，提高复用空间，应先考虑所提供的数据中有哪些可抽象的实体概念，而不是完全根据数据内容创建表。

1. 考点：考点应是独立的实体，具有考点号、考点名称两个字段
2. 学生：学生应是独立的实体，具有姓名字段（考虑到重名可能，应当添加学号）
3. 考试：在某个考场举行的考试，引用考点的考点号、考点名称字段，本身具有考场号、场次好、开考时间、指定试卷号
4. 准考证：某学生参与某场考试，引用考试的考点号、考场号、场次号（间接地引用了考点）字段，引用学生的姓名字段，本身具有考号、指定座位号

从引用关系的角度分析，考试基于考点，准考证基于考试和学生

从实体-关系的角度分析，则可以有多重理解：

1. 考点、考试、学生为实体，准考证表示的学生与考试之间的参与/包含关系
