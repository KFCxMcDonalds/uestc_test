import random

import pandas as pd
from pypinyin import lazy_pinyin
import question_2.efficiency as ef
import question_2.equilibrium as eq
import numpy as np

import q1_func


global select_flag  # 1:选择最佳均衡度 2:选择最佳效率
global N  # 种群数
global gene_num  # 基因数
global pinyin_list
global alphabet
global gen
global code_list
hanzi_file_path = "../question_1/Chinese.txt"  # 存储Chinese.txt文件的绝对路径
new_pinyin_file_path = "new_pinyin.txt"


def init_individual():
    global gene_num
    rand_list = []
    for i in range(gene_num):
        rand_list.append(i)

    # 非完全随机生成方式
    code = [0] * gene_num  # 所有声韵母的编码方式
    count = 0
    while count <= 1:
        for i in range(26):
            pos = random.choice(rand_list)
            while code[pos] != 0:
                pos = random.choice(rand_list)
            code[pos] = i
            rand_list.remove(pos)
        count += 1
    for pos in rand_list:
        code[pos] = random.sample(range(0, 26), 1)[0]

    # 完全随机生成方式
    # code = []
    # for i in range(gene_num):
    #     code.append(random.sample(range(26), 1)[0])

    return code


def init_population():
    # 生成个体数为N的新种群
    # gene_num个基因，即一个个体1*gene_num
    population = []  # 种群, 二维列表

    for i in range(N):
        individual = init_individual()
        population.append(individual)

    return population


def cross(father, mother):
    # 交叉算子：离散重组
    length = len(father)
    son = []
    for site in range(length):
        # 每一个位点随机选择父母中的某一个
        select = [father[site], mother[site]]
        gene = random.choice(select)
        son.append(gene)

    return son


def exchange(individual):
    sites = random.sample(range(gene_num), 2)
    tmp = individual[sites[1]]
    individual[sites[1]] = individual[sites[0]]
    individual[sites[0]] = tmp

    return individual


def reverse(individual):
    sites = random.sample(range(gene_num), 2)
    sites = sorted(sites)  # 从小到大
    tmp_list = individual[sites[0]:sites[1]]
    tmp_list.reverse()
    individual[sites[0]:sites[1]] = tmp_list  # 两个位点间逆序

    return individual


def mutant(individual):
    # 变异：互换变异 + 逆序变异
    individual = reverse(individual)
    individual = exchange(individual)

    return individual


def cross_and_mutant(popu, rate, fitness):
    # 需要生成N个新子代
    count = 0
    sons = []
    while count < N:
        parents = random.sample(range(N), 2)  # 父代中随机选择两个
        son = cross(popu[parents[0]], popu[parents[1]])  # 离散重组

        # 概率变异
        # 固定变异概率
        # flag = random.random()
        # if flag <= 0.1:
        #     son = mutant(son)  # 变异

        # 自适应变异概率
        pm_1 = 0.2  # 上限
        pm_2 = 0.1  # 下限
        flag = random.random()
        if fitness is list:
            # 该子代适应度
            son_fitness=[]
            gene_to_str(son)
            equi = eq.get_equilibrium(new_pinyin_file_path, gen)  # 均衡性
            effi = ef.get_efficiency(new_pinyin_file_path)  # 适应度
            son_fitness.append([equi, effi])

            son_f = son_fitness[0] * 10000 / son_fitness[1]
            sum = 0
            max = 0
            for i  in range(len(fitness)):
                tmp = fitness[0] * 10000 / fitness[1]
                sum += tmp
                if tmp > max:
                    max = tmp
            avg_f = sum / len(fitness)
            if son_f < avg_f:
                pm = pm_1
            else:
                pm = pm_1 - (pm_1 - pm_2) * (son_f - avg_f) / (max - avg_f)

            if flag <= pm:
                son = mutant(son)
        else:
            if flag <= 0.1:
                son = mutant(son)  # 变异

        sons.append(son)
        count += 1

    return sons


def get_pinyin_list():
    hanzi = open(hanzi_file_path, 'r').read()
    tmp = lazy_pinyin(hanzi)  # 获取拼音列表
    return tmp


def gene_to_str(individual):
    global code_list
    global alphabet
    new_pinyin_list = pinyin_list.copy()
    code_list = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z",
                 "x", "c", "v", "b", "n", "m", "zh", "ch", "sh", "iu", "ia", "ua", "uan", "ue", "ing", "uai", "uo",
                 "un", "iong", "ong", "iang", "uang", "en", "eng", "ang", "an", 'ao', 'ai', "ei", "ie", "iao", "ui",
                 "ou", "in", "ian"]
    zero_list = ["a", "ai", "an", "ang", "ao", "e", "ei", "en", "eng", "o", "ou"]
    two_list = ["zh", "ch", "sh"]
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']

    length = len(new_pinyin_list)
    for i in range(length):
        pinyin = new_pinyin_list[i]
        if pinyin[:2] in two_list:
            initials = pinyin[:2]
            finals = pinyin[2:]
            first = individual[code_list.index(initials)]
            second = individual[code_list.index(finals)]
            new_py = alphabet[first] + alphabet[second]
            new_pinyin_list[i] = new_py
        else:
            if pinyin in zero_list:
                new_pinyin_list[i] = pinyin[0] + pinyin
            pinyin = new_pinyin_list[i]
            initials = pinyin[0]
            finals = pinyin[1:]
            if finals == "ve":
                finals = "ue"
            first = individual[code_list.index(initials)]
            second = individual[code_list.index(finals)]
            new_py = alphabet[first] + alphabet[second]
            new_pinyin_list[i] = new_py

    new_pinyin_str = ''.join(new_pinyin_list)
    open(new_pinyin_file_path, 'w').write(new_pinyin_str)


def fast_non_dominated_sort(popu):
    # 快速非支配排序
    n = len(popu)
    np = [0] * n  # 被支配参数
    sp = [[] for i in range(n)]  # 支配个体
    fitness = []  # 两个适应度函数
    for i in range(n):
        gene_to_str(popu[i])
        equi = eq.get_equilibrium(new_pinyin_file_path, gen)  # 均衡性
        effi = ef.get_efficiency(new_pinyin_file_path)  # 适应度
        fitness.append([equi, effi])

    for i in range(n):
        for j in range(n):
            if j != i:
                if fitness[i][0] > fitness[j][0] and fitness[i][1] <= fitness[j][1]:
                    sp[i].append(j)  # j被i支配
                elif fitness[i][0] == fitness[j][0] and fitness[i][1] < fitness[j][1]:
                    sp[i].append(j)  # j被i支配
                elif fitness[i][0] == fitness[j][0] and fitness[i][1] > fitness[j][1]:
                    np[i] += 1  # i被j支配
                elif fitness[i][0] < fitness[j][0] and fitness[i][1] >= fitness[j][1]:
                    np[i] += 1  # i被j支配

    layer_num = 0
    length = len(np)
    compare = [-1] * length
    n_rank = [-1] * length
    F = [[]]  # 分层

    if 0 not in np:
        print("**已不可分层**")
        F[0] = np
    else:
        while np != compare:
            for i in range(length):
                if np[i] == 0:
                    n_rank[i] = layer_num
                    np[i] = -1
                    F[layer_num].append(i)
                    for k in sp[i]:
                        np[k] -= 1
            layer_num += 1
            F.append([])

    return n_rank, fitness, F


def crowding_degree(fitness):
    # 拥挤度计算
    fitness_1 = [i[0] for i in fitness]
    fitness_2 = [i[1] for i in fitness]

    length = len(fitness)
    n_d = [0] * length
    index_1 = sorted(range(length), key=lambda k: fitness_1[k])
    index_2 = sorted(range(length), key=lambda k: fitness_2[k])

    # 目标1排序
    for i in range(length):
        if i == 0 or i == length-1:
            ind = index_1[i]
            n_d[ind] += 1e6
        else:
            ind = index_1[i]
            n_d[ind] += fitness_1[index_1[i+1]] - fitness_1[index_1[i-1]]

    # 目标2排序
    for i in range(length):
        if i == 0 or i == length - 1:
            ind = index_2[i]
            n_d[ind] += 1e6
        else:
            ind = index_2[i]
            n_d[ind] += fitness_2[index_2[i+1]] - fitness_2[index_2[i-1]]

    return n_d


def elitist(popu, sons):
    for i in range(N):
        popu.append(sons[i])

    n_rank, fitness, F = fast_non_dominated_sort(popu)
    n_d = crowding_degree(fitness)

    length = len(F)
    num = 0
    kk = 0
    while(True):
        if num + len(F[kk]) > N:
            break
        num += len(F[kk])
        kk += 1

    # 老个体中可以组成新种群的个体序号
    new_popu_number = []
    for i in range(kk):
        new_popu_number += F[i]

    if num < 30:
        # 第kk层需要排序选择部分进入新种群
        individual_layer = F[kk]
        n_d_layer = []
        for j in individual_layer:
            n_d_layer.append(n_d[j])
        index = sorted(range(len(individual_layer)), key=lambda k: n_d_layer[k], reverse=True)
        tmp = np.array(F[kk])
        F[kk] = list(tmp[index])


        new_popu_number += F[kk][:N-num]

    # 组成新种群
    new_popu = []
    for j in new_popu_number:
        new_popu.append(popu[j])

    return new_popu, fitness


def show(popu):
    global gen
    global select_flag
    n = len(popu)
    fitness = []  # 两个适应度函数
    for i in range(n):
        gene_to_str(popu[i])
        equi = eq.get_equilibrium(new_pinyin_file_path, gen)  # 均衡性
        effi = ef.get_efficiency(new_pinyin_file_path)  # 适应度
        fitness.append([equi, effi])

    ind = -1

    if select_flag == 1:
        efficiency = [i[0] for i in fitness]
        ind = efficiency.index(max(efficiency))
    elif select_flag == 2:
        efficiency = [i[1] for i in fitness]
        ind = efficiency.index(min(efficiency))



    best_individual = popu[ind]
    gene_to_str(best_individual)

    # 均衡性和效率
    gen += 1  # 绘图
    effi = ef.get_efficiency(new_pinyin_file_path)
    equi = eq.get_equilibrium(new_pinyin_file_path, gen)

    df = pd.DataFrame()
    df['中文声韵母'] = code_list
    tmp = []
    for i in best_individual:
        tmp.append(alphabet[i])
    df['对应编码'] = tmp
    df.to_csv("output.csv", sep=',', header=True, index=True)
    print("****************************************************")
    print("**             output.csv输出文件已生成             **")
    str = "**           equilibrium is:%f              **" % (equi)
    print(str)
    str ="**         efficiency is:%f             **" % (effi)
    print(str)
    print("****************************************************")

    # 绘图
    pinyin_str = open(new_pinyin_file_path, 'r').read()
    q1_func.show_sta(pinyin_str)


if __name__ == "__main__":
    gen = 0
    select_flag = 1  # 当前：最佳均衡度
    pinyin_list = get_pinyin_list()
    N = 30  # 种群数=30
    gene_num = 55
    mutant_rate = 0.1
    popu = init_population()
    iter = 200  # 200代

    fitness = 0
    while gen <= 200:
        str = "当前运行第%d代" % gen
        print(str)

        sons = cross_and_mutant(popu, mutant_rate, fitness)
        new_popu, fitness = elitist(popu, sons)
        popu = new_popu
        gen += 1


    show(popu)

