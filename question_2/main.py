import efficiency
import equilibrium

pinyin_file_path = "../question_1/Pinyin.txt"
hanzi_file_path = "../question_1/Chinese.txt"


effi = efficiency.get_efficiency(pinyin_file_path)
equi = equilibrium.get_equilibrium(pinyin_file_path, 202)
print("****************************************************")
str = "**           equilibrium is:%f             **" % (equi)
print(str)
str ="**         efficiency is:%f            **" % (effi)
print(str)
print("****************************************************")


