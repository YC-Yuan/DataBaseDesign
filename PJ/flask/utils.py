import datetime


def string_to_date(string):
    return datetime.datetime.strptime(string, '%Y/%m/%d')


def string_to_timestamp(string):
    return datetime.time.mktime(datetime.time.strptime(string, '%Y-%m-%d %H:%M:%S'))


def get_current_timestamp():
    return datetime.datetime.now().timestamp()



