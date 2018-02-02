import pandas as pd
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import math


def dict_construct():
    """
    如何从两个list中构造dict
    """
    a = range(1,11)
    b = list("abcdefghij")
    mp = [(i,j) for i in a for j in b]
    print(dict(mp))
    """
    {1: 'j', 2: 'j', 3: 'j', 4: 'j', 5: 'j', 6: 'j', 7: 'j', 8: 'j', 9: 'j', 10: 'j'}
    """


def pandas_use():
    """
    使用pandas库中的read_csv读取csv数据
    """
    file_name = "jining/2018-01-01/part-00000"
    data = pd.read_csv(file_name, sep="\t",
                       names=["Female_id", "Male_id", "state", "male_popularity", "timestamp"])
    data = data.groupby(by = ['Male_id']).size()
    index = data.index
    for i in data.index:
        print(i, data.iloc(i))


def get_data(file_name):
    """
    使用csv库读取数据
    :param file_name:
    :return:
    """
    data = {}
    with open(file_name) as f:
        f_csv = csv.reader(f,delimiter='\t')
        for row in f_csv:
            if not row[1] in data.keys(): # 判断key是否在dict中
                data[row[1]] = 1
            else:
                data[row[1]] = data[row[1]] + 1
    #print(data)
    data = sorted(data.items(), key=lambda item:item[1], reverse=True)
    return [i[1] for i in data]

    #with open("output/male_statistic.csv","w") as f:
    #    for (male_id, num) in sorted_data:
    #        f.write(str(male_id) + "\t" + str(num) + "\n")

    #pd_data = pd.DataFrame(data)
    #pd_data.to_csv("male_statistic.csv")


def backup_merge_all_data():
    data_folder_name = "jining"
    data = pd.DataFrame([])
    finish_number = 0
    folders = os.listdir(data_folder_name)
    for dir in folders:
        for file in os.listdir(data_folder_name + "/" + dir):
            file_name = data_folder_name + "/" + dir + "/" + file
            file_data = pd.read_csv(file_name, sep="\t",
                       names=["Female_id", "Male_id", "state", "male_popularity", "timestamp"])
            data = pd.concat([data, file_data], axis=0, ignore_index=True)
        finish_number = finish_number + 1
        print("Reading... [" + str(finish_number) + "/" + str(len(folders)) + "]")
    print(data.groupby(by=['Male_id']).size())


def matplotlib_learn(data):
    """
    绘制长尾效应的折线图
    :param data:
    :return:
    """
    plt.plot(range(len(data)), data)
    plt.show()


def parse_csv_male_statistic():
    """
    从CSV中读取数据，绘制长尾效应的图表
    :return:
    """
    data = {}
    with open("output/male_statistic.csv") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data[row[0]] = int(row[1])
    return [item[1] for item in data.items()]


def parameter_test(data):
    """
    传入参数，对其值进行修改
    并没有返回这个参数

    外部是可以察觉到这个修改的
    """
    data[1] = 3

x = 3
def global_test():
    global x
    x = x + 1 # 4


def iter_test():
    a = [1,2,2,4]
    for i in range(len(a)):
        if a[i] == 2:
            del a[i]
    print(a)

def test_for_in():
    a = {1:2, 2:3}

    # 这是错误的做法
    #for (i,[j,k]) in a:
    #    print(i,j,k)

    for (i, j) in a.items():
        print(i,j)

def main():
    test_for_in()

if __name__ == "__main__":
    main()