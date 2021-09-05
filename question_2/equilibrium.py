import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 各手指控制的按键
I_list = ['y', 'h', 'n', 'u', 'j', 'm', 'r', 't', 'f', 'g', 'v', 'b']
M_list = ['e', 'd', 'c', 'i', 'k']
R_list = ['w', 's', 'x', 'o', 'l']
L_list = ['q', 'a', 'z', 'p']
# 各手指灵活度
finger_flex = [0.9448, 0.9327, 0.91645, 0.8676]


def get_pinyin_str(file):
    # 文件读出为字符串
    list = open(file, 'r').read()
    str = ''.join(list)
    return str


def finger_num(str):
    # 各手指控制按键出现的次数
    global I_dict, M_dict, R_dict, L_dict

    I_num, M_num, R_num, L_num = 0, 0, 0, 0
    I_dict = dict.fromkeys(I_list, 0)
    M_dict = dict.fromkeys(M_list, 0)
    R_dict = dict.fromkeys(R_list, 0)
    L_dict = dict.fromkeys(L_list, 0)

    for letter in str:
        if letter in I_list:
            I_dict[letter] += 1
            I_num += 1
        elif letter in M_list:
            M_dict[letter] += 1
            M_num += 1
        elif letter in R_list:
            R_dict[letter] += 1
            R_num += 1
        elif letter in L_list:
            L_dict[letter] += 1
            L_num += 1

    return [I_num, M_num, R_num, L_num]


def normalization(list):
    # 归一化
    divide = max(list) - min(list)
    list_nor = []
    for i in range(len(list)):
        list_nor.append((list[i] - min(list)) / divide)

    return list_nor


def theory_finger_nums(str):
    finger_flex_nor = normalization(finger_flex)
    finger_flex_nor.reverse()
    finger_rate = []
    finger_rate.append(0)
    for i in range(1, 4):
        finger_rate.append(finger_flex_nor[i] - finger_flex_nor[i-1])
    for i in range(4):
        # 每个手指相对于小指的比例倍数
        finger_rate[i] += 1
        if i >= 1:
            finger_rate[i] *= finger_rate[i-1]

    # 求解每个手指针对该文章理论最佳敲击数
    theory_fn_list = []
    L_theory_num = len(str) / sum(finger_rate)  # 小指理论值
    theory_fn_list.append(L_theory_num)
    for i in range(1, 4):
        theory_fn_list.append(finger_rate[i] * L_theory_num)
    theory_fn_list.reverse()
    return theory_fn_list


def compare_between_fingers(actual, theory):
    return np.corrcoef(actual, theory)[0, 1]  # 变化趋势的相似度


def compare_in_each_finger():
    I_var = np.std(list(I_dict.values()), ddof=0) / np.mean(list(I_dict.values()))
    M_var = np.std(list(M_dict.values()), ddof=0) / np.mean(list(M_dict.values()))
    R_var = np.std(list(R_dict.values()), ddof=0) / np.mean(list(R_dict.values()))
    L_var = np.std(list(L_dict.values()), ddof=0) / np.mean(list(L_dict.values()))

    return np.mean([I_var, M_var, R_var, L_var])


def image_plot(nums_of_each_finger):
    key_list = ['I', 'M', 'R', 'L']
    plt.figure(num=1, figsize=(12, 12))
    plt.subplot(3, 2, 1)
    plt.title("finger heatmap")
    df_num = pd.DataFrame({"number": nums_of_each_finger},
                            index=key_list)
    sns.heatmap(df_num, annot=False, cmap="RdBu_r")  # 手指使用的热力图

    plt.subplot(3, 2, 2)
    plt.title("finger line")
    df = pd.DataFrame()
    df['finger'] = key_list
    df['number'] = nums_of_each_finger
    sns.lineplot(data=df, x='finger', y='number')  # 手指使用折线图

    # 食指
    plt.subplot(3, 2, 3)
    df = pd.DataFrame()
    df['index finger'] = I_dict.keys()
    df['number'] = I_dict.values()
    sns.barplot(data=df, x='index finger', y='number')

    # 中指
    plt.subplot(3, 2, 4)
    df = pd.DataFrame()
    df['middle finger'] = M_dict.keys()
    df['number'] = M_dict.values()
    sns.barplot(data=df, x='middle finger', y='number')

    # 无名指
    plt.subplot(3, 2, 5)
    df = pd.DataFrame()
    df['Ring finger'] = R_dict.keys()
    df['number'] = R_dict.values()
    sns.barplot(data=df, x='Ring finger', y='number')

    # 小指
    plt.subplot(3, 2, 6)
    df = pd.DataFrame()
    df['Little finger'] = L_dict.keys()
    df['number'] = L_dict.values()
    sns.barplot(data=df, x='Little finger', y='number')

    plt.show()


def get_equilibrium(pinyin_file_path, gen):
    pinyin_str = get_pinyin_str(pinyin_file_path)
    nums_of_each_finger = finger_num(pinyin_str)  # 实际每个手指敲击数
    theory_nums_of_each_finger = theory_finger_nums(pinyin_str)  # 理论最佳每个手指敲击数
    equi_entire = compare_between_fingers(nums_of_each_finger, theory_nums_of_each_finger)  # 整体手指间的均衡性

    equi_each = compare_in_each_finger()  # 单个手指的均衡性
    equilibrium = equi_entire / equi_each

    if gen == 202:
        image_plot(nums_of_each_finger)

    return equilibrium

