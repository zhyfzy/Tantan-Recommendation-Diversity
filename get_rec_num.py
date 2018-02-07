"""
统计给每个人推荐的项目个数
"""
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def get_data(file_name, data):
    last_row_id = "-1"
    rec_times = 0
    with open(file_name) as f:
        f_csv = csv.reader(f,delimiter='\t')
        for row in f_csv:
            if row[0] != last_row_id:
                #record data
                if last_row_id != "-1":
                    if not last_row_id in data.values():
                        data[last_row_id] = 0
                    data[last_row_id] += rec_times
                #clear
                last_row_id = row[0]
                rec_times = 1
            else:
                rec_times += 1

        if last_row_id != "-1":
            if not last_row_id in data.values():
                data[last_row_id] = 0
            data[last_row_id] += rec_times


def statistic_data(data):
    """
    :param data: 每个id的推荐次数
    :return: 每个推荐次数，出现的次数
    """
    rec_num = {}
    for item in data.items():
        if not item[1] in rec_num.keys():
            rec_num[item[1]] = 1
        else:
            rec_num[item[1]] += 1
    return rec_num


def draw_plot(data):
    """
    横轴：一个人一天点击探探(like/dislike)的次数。纵轴：一个月内有多少这样的人
    """
    print(data.values())
    plt.bar(list(data.keys())[1:100], list(data.values())[1:100])
    plt.savefig("output/rec_num.eps")
    plt.show()


def gen_data():
    """
    读取数据，然后写入到文件中
    文件：两列
        一个人一天点击探探(like/dislike)的次数，
        一个月内有多少这样的人
    """
    data = {}

    # 对每个文件进行扫描
    data_folder_name = "jining"
    finish_number = 0
    folders = os.listdir(data_folder_name)
    for dir in folders:
        for file in os.listdir(data_folder_name + "/" + dir):
            file_name = data_folder_name + "/" + dir + "/" + file
            get_data(file_name, data)
        finish_number = finish_number + 1
        print("Reading... [" + str(finish_number) + "/" + str(len(folders)) + "]")

    print(data)
    rec_num = statistic_data(data)
    rec_num  = dict(sorted(rec_num.items(), key=lambda item:item[0]))
    print(rec_num)
    with open("output/rec_num.csv","w") as f:
        for (x, y) in rec_num.items():
            f.write(str(x) + "," + str(y) + "\n")

    draw_plot(rec_num)


def unit_test():
    """
    仅测试用
    """
    data = {}
    file_name = "jining/2018-01-01/part-00000"
    get_data(file_name, data)
    print(data)
    rec_num = statistic_data(data)
    rec_num  = dict(sorted(rec_num.items(), key=lambda item:item[0]))
    print(rec_num)
    with open("output/rec_num.csv","w") as f:
        for (x, y) in rec_num.items():
            f.write(str(x) + "," + str(y) + "\n")
    draw_plot(rec_num)



def draw_plot_x_y(x,y):
    """
    横轴：一个人一天点击探探(like/dislike)的次数。纵轴：一个月多于这个次数的百分比
    10 --> 75.54%
    20 --> 63.39%
    """
    num = "no_limit"
    plt.plot(x, y)
    plt.savefig("output/rec_num/cdf_" + str(num) + ".eps")
    plt.show()


def from_file_calc_cdf():
    """
    从gen_data产生的文件中读取数据，然后计算cdf
    """
    data = {}
    with open("output/rec_num/rec_num.csv", "r") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            data[int(row[0])] = int(row[1])
    tot_user = len(data)
    x = list(data.keys())
    data = np.array(list(data.values()))
    data = np.cumsum(data)
    # print(data[-1]) 总26480个女性用户
    data = 1.0 - (data[-1] - data) / data[-1]
    #print(data[-1])
    #print(x[20])
    #print(data[20] * 26480) # 每天刷20个以上的 --> 16768个用户
    draw_plot_x_y(x, data)


def main():
    """
    from_file_calc_cdf() or gen_data()
    """
    from_file_calc_cdf()


if __name__ == "__main__":
    main()