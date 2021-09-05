import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def sorted_by_key(d):
    # 将字典按键从小到大排序
    return sorted(d.items(), key=lambda k: k[0])


def sorted_by_value(d):
    # 将字典按值从小到大排序
    return sorted(d.items(), key=lambda k: k[1])


def statistics(str):
    nums_stat = {}  # 统计每个字母出现次数的字典
    # 统计频数
    for charactor in str:
        nums_stat[charactor] = str.count(charactor)

    value_list = list(dict.values(nums_stat))
    key_list = list(dict.keys(nums_stat))

    s = sum(value_list)  # 所有字母出现的总数

    rate_stat = nums_stat.copy()  # 统计每个字母出现频率的字典
    # 统计频率
    for key in key_list:
        rate_stat[key] /= s

    return nums_stat, rate_stat


def sort_alphabetically(rate_stat):
    # 按键从a-z排序
    rate_stat_key = dict(sorted_by_key(rate_stat))  # 按key排序

    value_list_bykey = list(dict.values(rate_stat_key))  # 排序好的值列表
    key_list_bykey = list(dict.keys(rate_stat_key))  # 排序好的键列表

    df_key = pd.DataFrame({"Rate": value_list_bykey},
                  index=key_list_bykey)

    return df_key


def sort_by_rate(rate_stat):
    # 按值从小到大排序
    rate_stat_value = dict(sorted_by_value(rate_stat))  # 按value排序

    value_list_byvalue = list(dict.values(rate_stat_value))  # 排序好的值列表
    key_list_byvalue = list(dict.keys(rate_stat_value))  # 排序好的键列表

    df_value = pd.DataFrame({"Rate": value_list_byvalue},
                  index=key_list_byvalue)

    return df_value


def heatmap_plot(df_key, df_value):
    # 绘图
    plt.figure(num=1, figsize=(7, 5))
    plt.subplot(1, 2, 1)
    plt.title("Alphabetically")
    sns.heatmap(df_key, annot=False, cmap="RdBu_r")  # 按字母顺序的热力图

    plt.subplot(1, 2, 2)
    plt.title("By frequency of use")
    sns.heatmap(df_value, annot=False, cmap="RdBu_r")  # 按使用频率的热力图
    plt.show()


def show_sta(pinyin_str):
    nums_stat, rate_stat = statistics(pinyin_str)
    df_key = sort_alphabetically(rate_stat)
    df_value = sort_by_rate(rate_stat)
    heatmap_plot(df_key, df_value)