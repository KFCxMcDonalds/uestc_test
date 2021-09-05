import xlrd
import math

finger_time_xlsx = "/Users/ivywu/Desktop/ivy/重要文件/电科保研/test/question_2/finger_time.xlsx"


def xlsx_process(path):
    # 手指键入时间当量处理成二维列表
    global finger_time_table
    xlsx = xlrd.open_workbook(path)
    sheet1 = xlsx.sheets()[0]
    rows = sheet1.nrows

    finger_time_table = []
    for i in range(rows):
        ele = sheet1.row_values(i)
        finger_time_table.append(ele)


def get_pinyin_str(file):
    # 文件读出为字符串
    list = open(file, 'r').read()
    str = ''.join(list)
    return str


def char_to_index(char):
    # 字母在时间当量表中的索引
    return ord(char) - 97


def theory_time(str):
    # 不考虑选词的理论最短时间
    time = 0
    for i in range(1, len(str)):
        row = char_to_index(str[i-1])
        col = char_to_index(str[i])
        time += finger_time_table[row][col]

    t0 = 0.18099  # 当量为1的具体时间

    return time * t0


def select_impact():
    return math.log(16.2, 2)


def get_efficiency(pinyin_file_path):
    xlsx_process(finger_time_xlsx)
    pinyin_str = get_pinyin_str(pinyin_file_path)
    time_least = theory_time(pinyin_str)
    time_actual = time_least * select_impact()

    return time_actual
