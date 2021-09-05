import efficiency
import equilibrium

pinyin_file_path = "/Users/ivywu/Desktop/ivy/重要文件/电科保研/test/question_1/Pinyin.txt"
hanzi_file_path = "/Users/ivywu/Desktop/ivy/重要文件/电科保研/test/question_1/Chinese.txt"


effi = efficiency.get_efficiency(pinyin_file_path)
equi = equilibrium.get_equilibrium(pinyin_file_path, 102)
str = "equilibrium is:%f\nefficiency is:%f" % (equi, effi)
print(str)

