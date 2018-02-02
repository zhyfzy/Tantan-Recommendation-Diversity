"""
使用Re-Rank方法提高多样性
根据物品的受欢迎程度重新排序
"""
import csv
import os
import matplotlib.pyplot as plt


male_stc = {}

TOP_N = 10
T_R = 9
T_H = 20
PRE = T_R - TOP_N
TOT_MALES = 801948
FILE_NAME = "output/Rerank-absolute-like/Rerank_likenum_" + str(T_R) + "_20"

"""
acc T_H = 0 --> 10
-0.12474555080933192
-0.014229833019198512
0.09682651234597153
0.20825925119102912
0.31989221545543145
0.43129843437738424
0.5435964804273514
0.6563436603177227
0.7699872136085141
0.8841613547895754
1.0
"""


class MalePopularity(object):
    def __init__(self):
        popularity_file = "output/Male_liked_num.csv"
        self.data = {}
        popularity = 801948
        with open(popularity_file, "r") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                self.data[row[0]] = popularity # 越受欢迎， popularity值越大
                popularity -= 1

    def get_popularity(self, rank):
        if not rank in self.data.keys():
            return 0
        return self.data[rank]


male_popularity = MalePopularity()

user_num = 0
tot_acc = .0

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
        row.append(rating)
        rating -= 1

    # 排序，使得热度不高的人在前边
    data = sorted(data, key=lambda x:male_popularity.get_popularity(x[1]))
    # 调整，去除掉rating小于T_R的
    target = [item for item in data if item[5] >= T_R][:TOP_N]
    assert(len(target) == TOP_N)
    target_rating = [item[5] for item in target]

    for row in target:
        if row[1] in male_stc.keys():
            male_stc[row[1]] += 1
        else:
            male_stc[row[1]] = 1

    # 计算 acc
    acc = 0
    for i in range(T_H - 1, -1, -1):
        if not i in target_rating:
            acc += len([j for j in target_rating if j>i])
            acc -= len([j for j in target_rating if j<i])

    acc = acc / ((T_H - TOP_N) * TOP_N)
    global tot_acc
    global user_num
    tot_acc += acc
    user_num += 1


def end_parse_male_statistic():
    """
    在结束的时候处理
    """
    sorted_data = sorted(male_stc.items(), key=lambda item:item[1], reverse=True)
    with open(FILE_NAME + ".csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num) + "\n")
    print("T_R:" + str(T_R))
    print("acc: " + str(tot_acc / user_num))
    draw_plot([item[1] for item in sorted_data])


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
    plt.plot(range(len(data))[:200], data[:200])
    plt.xlabel("Rank")
    plt.ylabel("Recommend times")
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
