import csv
import matplotlib.pyplot as plt

def get_data(T_R):
    FILE_NAME = "output/Rerank-absolute-like/Rerank_likenum_" + str(T_R) + "_20"

    popularity = []
    with open(FILE_NAME + ".csv", "r") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            popularity.append(int(row[1]))
    return popularity


def add_figure(axes, T_R, color, label):
    popularity = get_data(T_R)
    axes.plot(range(len(popularity))[:200],
              popularity[:200], color,
              label=label)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

fig = plt.figure()
axes = fig.add_axes([0.15, 0.15, 0.8, 0.8])

add_figure(axes, 7, "m", "T_R = 7")
add_figure(axes, 8, "b", "T_R = 8")
add_figure(axes, 9, "k", "T_R = 9")
add_figure(axes, 10, "g", u"原始数据")
axes.set_xlabel(u"用户按照被推荐次数从大到小排序")
axes.set_ylabel(u"推荐次数")
fig.legend(loc=(0.75,0.73))
fig.savefig("output/Result_compare.pdf")
plt.show()