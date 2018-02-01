"""
统计每个用户被推荐的次数
"""
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import os
import csv
import matplotlib.pyplot as plt

data = {}

def get_data(file_name):
    with open(file_name) as f:
        f_csv = csv.reader(f,delimiter='\t')
        for row in f_csv:
            if not row[1] in data.keys(): # 判断key是否在dict中
                data[row[1]] = 1
            else:
                data[row[1]] = data[row[1]] + 1


def draw_plot(data):
    plt.plot(range(len(data)), data)
    plt.savefig("output/male_statistic.eps")
    plt.show()


def unit_test():
    pass


def main():
    data_folder_name = "jining"
    finish_number = 0
    folders = os.listdir(data_folder_name)
    for dir in folders:
        for file in os.listdir(data_folder_name + "/" + dir):
            file_name = data_folder_name + "/" + dir + "/" + file
            get_data(file_name)
        finish_number = finish_number + 1
        print("Reading... [" + str(finish_number) + "/" + str(len(folders)) + "]")
    sorted_data = sorted(data.items(), key=lambda item:item[1], reverse=True)
    with open("output/male_statistic.csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num) + "\n")
    draw_plot([item[1] for item in sorted_data])


if __name__ == "__main__":
    main()
