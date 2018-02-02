"""
使用Re-Rank方法提高多样性
根据物品的受欢迎程度重新排序
"""
import csv
import os
import matplotlib.pyplot as plt


male_stc = {}

FILE_NAME = "output/Male_relative_like"


def parse(data):
    """
    在get_data中读取数据，送入到parse中，在这里进行统计
    """
    if data[1] in male_stc.keys():
        if not data[2] == "disliked":
            male_stc[data[1]][0] += 1
        male_stc[data[1]][1] += 1
    else:
        male_stc[data[1]] = [0,1]
        if not data[2] == "disliked":
            male_stc[data[1]][0] = 1


def end_parse_male_statistic():
    """
    在结束的时候处理
    """
    sorted_data = sorted(male_stc.items(), key=lambda item:item[1][0]/item[1][1], reverse=True)
    with open(FILE_NAME + ".csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num[0] / num[1]) + "\n")
    draw_plot([item[1][0]/item[1][1] for item in sorted_data])


def get_data(file_name):
    with open(file_name) as f:
        f_csv = csv.reader(f,delimiter='\t')
        for row in f_csv:
            parse(row)


def draw_plot(data):
    print(len(data))
    plt.plot(range(len(data)), data)
    plt.savefig(FILE_NAME + ".eps")
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


def from_file():
    males = []
    popularity = []
    with open(FILE_NAME + ".csv", "r") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            males.append(int(row[0]))
            popularity.append(int(row[1]))
    draw_plot(popularity)


if __name__ == "__main__":
    main()
