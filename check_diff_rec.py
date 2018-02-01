"""
检测是否会多次推荐同一个人

经过测试，是会给同一个人多次推荐另外一个人
需要对数据进行筛选
"""

import csv
import os
import matplotlib.pyplot as plt

T_H = 20
T_R = 20
TOP_N = 20

male_stc = {}


def parse(data):
    """
    在get_data中读取数据，送入到parse中，在这里进行统计
    """
    males = []
    for row in data:
        if row[1] in males:
            print(row[1])
            print(data)
            break
        else:
            males.append(row[1])


def end_parse_male_statistic():
    """
    在结束的时候处理
    """
    sorted_data = sorted(male_stc.items(), key=lambda item:item[1], reverse=True)
    with open("output/front" + str(TOP_N) + "_male_statistic.csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num) + "\n")
    draw_plot([item[1] for item in sorted_data])


def get_data(file_name):
    last_row_id = "-1"
    rec_times = 0
    row_list = []
    with open(file_name) as f:
        f_csv = csv.reader(f,delimiter='\t')
        for row in f_csv:
            if row[0] != last_row_id:
                # record data
                if last_row_id != "-1":
                    row_list = sorted(row_list, key=lambda x:int(x[4]))[:TOP_N]
                    if len(row_list) == TOP_N:
                        parse(row_list)

                # clear
                last_row_id = row[0]
                rec_times = 1
                row_list = [row]
            else:
                rec_times += 1
                row_list.append(row)

        if last_row_id != "-1":
            row_list = sorted(row_list, key=lambda x: int(x[4]))[:TOP_N]
            if len(row_list) == TOP_N:
                parse(row_list)


def draw_plot(data):
    plt.plot(range(len(data)), data)
    plt.savefig("output/front20_male_statistic.eps")
    plt.show()


def unit_test():
    """
    仅测试用
    """
    file_name = "jining/2018-01-01/part-00000"
    get_data(file_name)
    end_parse_male_statistic()


def main():
    # 对每个文件进行扫描
    data_folder_name = "jining"
    finish_number = 0
    folders = os.listdir(data_folder_name)
    for dir in folders:
        for file in os.listdir(data_folder_name + "/" + dir):
            file_name = data_folder_name + "/" + dir + "/" + file
            get_data(file_name)
        finish_number = finish_number + 1
        print("Reading... [" + str(finish_number) + "/" + str(len(folders)) + "]")
    end_parse_male_statistic()


if __name__ == "__main__":
    main()
