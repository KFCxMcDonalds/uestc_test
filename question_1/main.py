from pypinyin import lazy_pinyin
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import re
import os

input_path = "共产党宣言.txt"
hanzi_file_path = "Chinese.txt"
pinyin_file_path = "Pinyin.txt"



def sorted_by_key(d):
    # 将字典按键从小到大排序
    return sorted(d.items(), key=lambda k: k[0])


def sorted_by_value(d):
    # 将字典按值从小到大排序
    return sorted(d.items(), key=lambda k: k[1])


def article_to_hanzi(inputfile):
    # 原文件中提取汉字
    if os.path.isfile(hanzi_file_path):
        os.remove(hanzi_file_path)
    article = open(inputfile, 'r').read()
    hanzi = re.findall(r'[\u4e00-\u9fa5]+', article)  # unicode编码中的简体汉字
    for c in hanzi:
        open(hanzi_file_path, 'a').write(c)


def hanzi_to_pinyin(inputfile):
    # 汉字转换成拼音字符串
    if os.path.isfile(pinyin_file_path):
        os.remove(pinyin_file_path)
    hanzi = open(inputfile, 'r').read()
    pinyin_list = lazy_pinyin(hanzi)  # 获取拼音列表
    pinyin_str = ''.join(pinyin_list)  # 所有拼音组成一个字符串

    # 写入文件
    open(pinyin_file_path, 'w').write(pinyin_str)
    return pinyin_str


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


if __name__ == "__main__":
    article_to_hanzi(input_path)
    pinyin_str = hanzi_to_pinyin(hanzi_file_path)
    nums_stat, rate_stat = statistics(pinyin_str)
    df_key = sort_alphabetically(rate_stat)
    df_value = sort_by_rate(rate_stat)
    heatmap_plot(df_key, df_value)

