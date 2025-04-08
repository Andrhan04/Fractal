import scipy.stats as stats
from scipy.stats import shapiro
from scipy.stats import normaltest
from collections import namedtuple
import numpy as np

# 1. Проверка на показательное распределение
def test_exponential(data, alpha = 0.05):
    # Определим параметр λ
    lambda_param = 1 / np.mean(data)
    # Определение интервального распределения
    bins = np.histogram_bin_edges(data, bins='auto')
    observed_freq, _ = np.histogram(data, bins=bins)
    # Теоретические частоты для показательного распределения
    expected_freq = len(data) * (np.diff(bins) * lambda_param * np.exp(-lambda_param * bins[:-1]))
    # Вычисляем значение критерия χ²
    chi_squared = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    # Степени свободы: количество интервалов - 1
    df = len(observed_freq) - 1
    critical_value = stats.chi2.ppf(1 - alpha, df)
    
    print(f'Показательное распределение: χ² = {chi_squared:.4f}, критическое значение = {critical_value:.4f}')
    if(chi_squared > critical_value):
        print('гипотеза отклоняется')
    else:
        print('нет оснований отвергать гипотезу ')
    return chi_squared, critical_value, chi_squared > critical_value

# 2. Проверка на равномерное распределение
def test_uniform(data, alpha = 0.05):
    # Определение диапазона данных
    min_val, max_val = np.min(data), np.max(data)
    bins = np.linspace(min_val, max_val, 6)  # 5 интервалов для равномерного распределения
    observed_freq, _ = np.histogram(data, bins=bins)
    
    # Теоретические частоты для равномерного распределения
    expected_freq = len(data) / len(observed_freq) * np.ones_like(observed_freq)

    # Вычисляем значение критерия χ²
    chi_squared = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    
    # Степени свободы
    df = len(observed_freq) - 1
    critical_value = stats.chi2.ppf(1 - alpha, df)
    
    print(f'Равномерное распределение: χ² = {chi_squared:.4f}, критическое значение = {critical_value:.4f}')
    if(chi_squared > critical_value):
        print('гипотеза отклоняется')
    else:
        print('нет оснований отвергать гипотезу ')
    return chi_squared, critical_value, chi_squared > critical_value

f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
f.close()

#       Частицы
# чтение из файла
F = open("log\\pole_" + str(id_pole) + "\\Points_" + str(id_point) + "\\Alive_" + str(id_exp) + ".txt",'r+')
data = []
data = F.readlines()
F.close()
# обработка данных
pt_x = []
pt_y = []
for s in data:
    buf = s.split()
    pt_x.append(int(float(buf[0]))//50)
    pt_y.append(int(float(buf[1]))//50)

data_x = [0]*(max(pt_x)+1)
for i in pt_x:
    data_x[i]+=1

data_y = [0]*(max(pt_y)+1)
for i in pt_y:
    data_y[i]+=1

#-- класс для неприменимости метода
MethodNotAllowed = namedtuple('MethodNotAllowed', ['statistic', 'pvalue'])
methodNotAllowed=MethodNotAllowed("D'Agostino not works!","D'Agostino not works!")

if len(data_y)!=0:
    #считаем нормальность распределения
    label="None"
    if len(data_y)>=3:
        ResShapiro=shapiro(data_y)
    else:
        ResDAgostino=methodNotAllowed
    if len(data_y)>=20:
        ResDAgostino=normaltest(data_y)
    else:
        ResDAgostino=methodNotAllowed
    #line=str(len(data_y))+";"+str(label)+";"+str(ResShapiro.statistic)+";"+str(ResShapiro.pvalue)+";"+str(ResDAgostino.statistic)+";"+str(ResDAgostino.pvalue)
    #считаем дисперсию и стандартное отклонение
    line=str(np.var(data_y))+";"+str(np.std(data_y))+";"+str(max(data_y)-min(data_y))
    line=line+'\n'
print("FOR Y")
print("ResShapiro.statistic    = " + str(ResShapiro.statistic))     # Должно к 1 стремиться
print("ResShapiro.pvalue       = " + str(ResShapiro.pvalue))        # Значение p для проверки гипотезы
print("ResDAgostino.statistic  = " + str(ResDAgostino.statistic))   # Должно к 1 стремиться
print("ResDAgostino.pvalue     = " + str(ResDAgostino.pvalue))      # Значение p для проверки гипотезы
test_uniform(data_y)
test_exponential(data_y)


if len(data_x)!=0:
    #считаем нормальность распределения
    label="None"
    if len(data_x)>=3:
        ResShapiro=shapiro(data_x)
    else:
        ResDAgostino=methodNotAllowed
    if len(data_x)>=20:
        ResDAgostino=normaltest(data_x)
    else:
        ResDAgostino=methodNotAllowed
    #line=str(len(data_y))+";"+str(label)+";"+str(ResShapiro.statistic)+";"+str(ResShapiro.pvalue)+";"+str(ResDAgostino.statistic)+";"+str(ResDAgostino.pvalue)
    #считаем дисперсию и стандартное отклонение
    line=str(np.var(data_x))+";"+str(np.std(data_x))+";"+str(max(data_x)-min(data_x))
    line=line+'\n'

print("FOR X")
print("ResShapiro.statistic    = " + str(ResShapiro.statistic))     # Должно к 1 стремиться
print("ResShapiro.pvalue       = " + str(ResShapiro.pvalue))        # Значение p для проверки гипотезы
print("ResDAgostino.statistic  = " + str(ResDAgostino.statistic))   # Должно к 1 стремиться
print("ResDAgostino.pvalue     = "+str(ResDAgostino.pvalue))        # Значение p для проверки гипотезы
test_uniform(data_x)
test_exponential(data_x)