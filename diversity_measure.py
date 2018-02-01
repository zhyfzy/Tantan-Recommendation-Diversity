"""
测量多样性
"""

import csv
import os
import matplotlib.pyplot as plt
import numpy as np

T_H = 20
T_R = 20
TOP_N = 10

male_stc = {}

def from_file(filename):
    """
    输入为front20_male_statistic输出的文件
    """
    ans = 0
    l = 0
    with open(filename, "r") as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            l += 1
            num = int(row[1])
            ans += (num * num - num)//2
    print(ans/20/(l*(l-1)//2))


def main():
    # 对每个文件进行扫描
    from_file("output/Rerank_popularity_0_20.csv")


if __name__ == "__main__":
    main()
