"""
得到每个男性用户的平均rating值
"""
import csv
import os
import matplotlib.pyplot as plt


male_stc = {}

TOP_N = 10
T_R = 0
T_H = 20
PRE = T_R - TOP_N
TOT_MALES = 801948
FILE_NAME = "output/Male_average_rating"


def parse(data):
    """
    在get_data中读取数据，送入到parse中，在这里进行统计
    """

    # 只取前TOP_N个推荐
    data = data[:T_H]
    if not len(data) == T_H:
        return

    # 为每个推荐标记线性rating，越靠前值越大
    rating = T_H - 1
    for row in data:
        if row[1] in male_stc.keys():
            male_stc[row[1]][0] += rating
            male_stc[row[1]][1] += 1
        else:
            male_stc[row[1]] = [rating, 1]
        rating -= 1


def end_parse_male_statistic():
    """
    在结束的时候处理
    """
    sorted_data = sorted(male_stc.items(), key=lambda item:item[1][0]/item[1][1], reverse=True)
    with open(FILE_NAME + ".csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num[0]/num[1]) + "\n")
    draw_plot([item[1][0]/item[1][1] for item in sorted_data])


def filter(data):
    """
    可能存在给一个人推荐多次同一个人，
    过滤掉这种情况
    """
    males = []
    filtered = []
    for item in data:
        if not item[1] in males:
            filtered.append(item)
            males.append(item[1])
    return filtered


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
                    row_list = sorted(row_list, key=lambda x:int(x[4]))
                    filtered = filter(row_list)
                    parse(filtered)

                # clear
                last_row_id = row[0]
                rec_times = 1
                row_list = [row]
            else:
                rec_times += 1
                row_list.append(row)

        if last_row_id != "-1":
            row_list = sorted(row_list, key=lambda x: int(x[4]))
            filtered = filter(row_list)
            parse(filtered)


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
