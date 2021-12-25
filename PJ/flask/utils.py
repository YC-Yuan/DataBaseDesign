import datetime


def string_to_date(string):
    return datetime.datetime.strptime(string, '%Y/%m/%d')


def get_current_timestamp():
    return datetime.datetime.now().timestamp()



