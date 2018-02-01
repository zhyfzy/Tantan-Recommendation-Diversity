"""
前20个推荐中，男性用户被推荐的统计

将数据按照时间排序
然后取前20个作为推荐备选

其前10个为系统推荐

这个项目的目标是：对20个推荐备选重新排序，使得前10个推荐的多样性上升
"""
import csv
import os
import matplotlib.pyplot as plt

TOP_N = 10

male_stc = {}


def parse(data):
    """
    在get_data中读取数据，送入到parse中，在这里进行统计
    """
    for row in data:
        if row[1] in male_stc.keys():
            male_stc[row[1]] += 1
        else:
            male_stc[row[1]] = 1


def end_parse_male_statistic():
    """
    在结束的时候处理
    """
    sorted_data = sorted(male_stc.items(), key=lambda item:item[1], reverse=True)
    with open("output/front" + str(TOP_N) + "_male_statistic.csv","w") as f:
        for (male_id, num) in sorted_data:
            f.write(str(male_id) + "," + str(num) + "\n")
    draw_plot([item[1] for item in sorted_data])



def filter(data):
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
                    filtered = filter(row_list)[:TOP_N]
                    if len(filtered) == TOP_N:
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
            filtered = filter(row_list)[:TOP_N]
            if len(filtered) == TOP_N:
                parse(filtered)


def draw_plot(data):
    print(len(data))
    plt.plot(range(len(data)), data)
    plt.savefig("output/front" + str(TOP_N) + "_male_statistic.eps")
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
    with open("output/front" + str(TOP_N) + "_male_statistic.csv", "r") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            males.append(int(row[0]))
            popularity.append(int(row[1]))
    draw_plot(popularity)


if __name__ == "__main__":
    main()
