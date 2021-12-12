import sys
import pandas as pd
import numpy
import time
import csv_read
import db_api

category = ''
filename = ''


def check_argv():
    if len(sys.argv) != 3:
        print("""请给出必要的两个参数,用空格隔开
        第一个参数可选room或student,表示载入的数据种类
        第二个参数需输入数据位置,如room.csv""")
        exit(0)
    global category
    global filename
    category = sys.argv[1]
    filename = sys.argv[2]
    if category not in ['student', 'room']:
        print("""请修改参数一,目前只能识别room和student""")
        exit(0)
    if filename[-4:] != '.csv':
        print("""请修改参数二,目前仅支持csv文件""")
        exit(0)


def check_registno(registno):
    if type(registno) is numpy.int64 and 100000 <= registno <= 999999:
        return True
    else:
        return False


def check_seat(seat):
    if type(seat) is numpy.int64 and seat <= 999:
        return True
    else:
        return False


def check_kdno(kdno):
    if type(kdno) is numpy.int64 and 1000 <= kdno <= 9999:
        return True
    else:
        return False


def check_kcno(kcno):
    if type(kcno) is numpy.int64 and kcno <= 9999:
        return True
    else:
        return False


def check_ccno(ccno):
    if type(ccno) is numpy.int64 and ccno <= 9999:
        return True
    else:
        return False


def check_str_20(text):
    return type(text) is str and len(text) <= 20


def check_time(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y/%m/%d %H:%M")
        else:
            time.strptime(date, "%Y/%m/%d")
        return True
    except:
        return False


def print_room_info():
    print(
        """room数据应有6列,分别为
kdno(4位数字)
kcno(4位以下数字)
ccno(4位以下数字)
kdname(20字以内)
exptime(形如"2004/6/10 16:40"的时间)
papername(20字以内)""")


def print_student_info():
    print(
        """room数据应有6列,分别为
registno(6位数字)
name(20字以内)
kdno(4位数字)
kcno(4位以下数字)
ccno(4位以下数字)
seat(4位以下数字)""")


if __name__ == '__main__':
    db_api.init_tables()
    check_argv()
    df = csv_read.read_csv(filename)
    if category == 'room':  # 处理考试信息
        col_num = csv_read.get_df_cols(df)
        # 检测表头
        room_heads = ['kdno', 'kcno', 'ccno', 'kdname', 'exptime', 'papername']
        for head in room_heads:
            if head not in df.loc[0]:
                print_room_info()
                exit(0)
        # 逐行检测合法性并写入信息
        db = db_api.get_db()
        cursor = db.cursor()
        try:
            for i in range(0, csv_read.get_df_rows(df)):
                data = df.loc[i]
                kdno = data['kdno']
                kcno = data['kcno']
                ccno = data['ccno']
                kdname = data['kdname']
                exptime = data['exptime']
                papername = data['papername']
                if pd.isnull(papername):  # 允许为空
                    print("第%d行papername未设置,请检查" % (i + 1))
                    papername = ""
                if check_kdno(kdno) and check_kcno(kcno) and check_ccno(ccno) \
                        and check_str_20(kdname) and check_time(exptime) \
                        and check_str_20(papername):  # 写入数据
                    # 写入考点
                    sql = db_api.get_kd(kdno)
                    cursor.execute(sql)
                    kd = cursor.fetchone()
                    if kd == None:  # 无此记录,插入
                        sql = db_api.insert_kd(kdno=kdno, kd_name=kdname)
                        cursor.execute(sql)
                    else:  # 已有记录,此时检查是否匹配新数据
                        if kd[1] != kdname:
                            print('一个考点编号只能对应一个数据,请比对数据是否与"%d,%s"冲突' % (kd[0], kd[1]))
                            print(data)
                            raise Exception()
                    # 写入考试
                    sql = db_api.insert_exam(kdno, kcno, ccno, exptime, papername)
                    cursor.execute(sql)
                else:
                    print('数据不符合格式要求')
                    print(data)
                    raise Exception()
        except Exception as e:
            print_room_info()
            db.rollback()
            exit(0)
        db.commit()
        cursor.close()
        db.close()
        print('写入数据成功')
    else:  # 处理学生信息
        col_num = csv_read.get_df_cols(df)
        # 检测表头
        room_heads = ['registno', 'name', 'kdno', 'kcno', 'ccno', 'seat']
        for head in room_heads:
            if head not in df.loc[0]:
                if head not in df.loc[0]:
                    print_student_info()
        # 逐行检测合法性并写入信息
        db = db_api.get_db()
        cursor = db.cursor()
        try:
            for i in range(0, csv_read.get_df_rows(df)):
                data = df.loc[i]
                registno = data['registno']
                name = data['name']
                seat = data['seat']
                kdno = data['kdno']
                kcno = data['kcno']
                ccno = data['ccno']
                if check_kdno(kdno) and check_kcno(kcno) and check_ccno(ccno) \
                        and check_registno(registno) and check_str_20(name) \
                        and check_seat(seat):  # 写入数据
                    # 写入学生
                    sql = db_api.get_student(registno=registno)
                    cursor.execute(sql)
                    student = cursor.fetchone()
                    if student == None:
                        sql = db_api.insert_student(registno=registno, stu_name=name)
                        cursor.execute(sql)
                    else:  # 已有记录,检查是否匹配
                        if student[1] != name:
                            print('一个准考证号只能对应一位学生,请对比数据是否与"%d,%s"冲突' % (student[0], student[1]))
                            print(data)
                            raise Exception
                    # 写入准考证
                    sql = db_api.get_exam_takes(registno=registno, kdno=kdno, kcno=kcno, ccno=ccno)
                    cursor.execute(sql)
                    et = cursor.fetchone()
                    if et == None:
                        try:
                            sql = db_api.insert_exam_takes(registno, seat, kdno, kcno, ccno)
                            cursor.execute(sql)
                        except:
                            print(data)
                            print("准考证插入失败,请检查是否已录入对应考点与考试")
                            db.rollback()
                            exit(0)
                    else:
                        print('第%d行存在重复的准考信息' % (i + 1))
                        print(data)
                else:
                    print("数据不符合格式要求")
                    print(data)
                    raise Exception()
        except Exception as e:
            print(e)
            print_student_info()
            db.rollback()
            exit(0)
        db.commit()
        cursor.close()
        db.close()
        print('写入数据成功')
    pass
