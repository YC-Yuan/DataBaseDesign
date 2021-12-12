import chardet
import pandas as pd

f_room = 'room.csv'
f_stu = 'student.csv'


def read_csv(filename):
    try:
        f = open(filename, mode='rb')
        data = f.read()
        f = chardet.detect(data)['encoding']
        data = pd.read_csv(filename, encoding=f)
        return data
    except:
        print('读取文件失败,请检查文件路径')
        exit(0)


def get_df_cols(df):
    return df.shape[1]


def get_df_rows(df):
    return df.shape[0]


if __name__ == '__main__':
    df = read_csv(f_room)
    print(df.shape[1])
