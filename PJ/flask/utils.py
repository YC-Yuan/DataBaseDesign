import datetime
import time
from constants.info import *


#   字符串转日期
def string_to_date(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d')


#   日期转字符串
def date_to_string(date):
    return date.strftime('%Y-%m-%d')


#   字符串转时间戳
def string_to_timestamp(string):
    return time.mktime(time.strptime(string, '%Y-%m-%d %H:%M:%S'))


#   时间戳转字符串
def timestamp_to_string(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


#   获取当前时间戳
def get_current_timestamp():
    return datetime.datetime.now()


#   获取当前时间戳
def get_current_date():
    return datetime.datetime.now() - datetime.timedelta(days=1)


#   检测是否结课
def check_course_end(date):
    return (datetime.datetime.now() - datetime.timedelta(days=1)).date() >= date


def dict_fetch_one(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row is None:
        return None
    else:
        tmp = list(row)
        return dict(zip(columns, tmp))


def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    # for row in cursor.fetchall():
    #     print(row)
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
