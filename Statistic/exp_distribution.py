import scipy.stats as stats
from scipy.stats import shapiro
from scipy.stats import normaltest
from collections import namedtuple
import numpy as np
import pandas as pd
import json
import os

# pip install pandas xlsxwriter openpyxl faker scipy numpy
# код для проверки критериев о распределении по итерациям

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
    
    # # print(f'Показательное распределение: χ² = {chi_squared:.4f}, критическое значение = {critical_value:.4f}')
    # if(chi_squared > critical_value):
    #     # print('гипотеза отклоняется')
    # else:
    #     # print('нет оснований отвергать гипотезу ')
    return chi_squared, critical_value, chi_squared < critical_value

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
    
    # # print(f'Равномерное распределение: χ² = {chi_squared:.4f}, критическое значение = {critical_value:.4f}')
    # if(chi_squared > critical_value):
    #     # print('гипотеза отклоняется')
    # else:
    #     # print('нет оснований отвергать гипотезу ')
    return chi_squared, critical_value, chi_squared < critical_value

# 3. Проверка на нормальное распределение распределение Шапиро
def test_normal_Shapiro(data):
    #-- класс для неприменимости метода
    MethodNotAllowed = namedtuple('MethodNotAllowed', ['statistic', 'pvalue'])
    methodNotAllowed=MethodNotAllowed("D'Agostino not works!","D'Agostino not works!")
    if len(data)!=0:
        #считаем нормальность распределения
        label="None"
        if len(data)>=3:
            ResShapiro=shapiro(data)
        else:
            ResShapiro=methodNotAllowed
    return ResShapiro

# 4. Проверка на нормальное распределение распределение Д`Агостино
def test_normal_DAgostino(data):
    #-- класс для неприменимости метода
    MethodNotAllowed = namedtuple('MethodNotAllowed', ['statistic', 'pvalue'])
    methodNotAllowed=MethodNotAllowed("D'Agostino not works!","D'Agostino not works!")
    if len(data)!=0:
        #считаем нормальность распределения
        label="None"
        if len(data)>=20:
            ResDAgostino=normaltest(data)
        else:
            ResDAgostino=methodNotAllowed
    return ResDAgostino


#----------------------------------------------------------------------------------------------------------------
# Память
stats_value_y = {'iteration' : [], 'alpha' : [],
                 'Shapiro.stats' : [],         'Shapiro.p_value' : [], 
                 "DAgostino.stats":[],         "DAgostino.p_value":[],
                 'Uniform.observable' : [],    "Uniform.critical":[], 
                 "Exponential.observable":[],  "Exponential.critical":[]
                 }
stats_value_x = {'iteration' : [], 'alpha' : [],
                 'Shapiro.stats' : [],         'Shapiro.p_value' : [], 
                 "DAgostino.stats":[],         "DAgostino.p_value":[],
                 'Uniform.observable' : [],    "Uniform.critical":[], 
                 "Exponential.observable":[],  "Exponential.critical":[]
                 }
stats_work_y = {'iteration' : [], 'Shapiro' : [], 'DAgostino' : [], 'Uniform' : [],  'Exponential': []}
stats_work_x = {'iteration' : [], 'Shapiro' : [], 'DAgostino' : [], 'Uniform' : [],  'Exponential': []}


#----------------------------------------------------------------------------------------------------------------
def programm(path, file, step, alpha):
    # открытие файла
    F = open(path + '/' + file,'r+')
    data = []
    data = F.readlines()
    F.close()
    # обработка данных
    pt_x = []
    pt_y = []
    for s in data:
        buf = s.split()
        pt_x.append(int(float(buf[0]))//step)
        pt_y.append(int(float(buf[1]))//step)

    data_x = [0]*(max(pt_x)+1)
    for i in pt_x:
        data_x[i]+=1

    data_y = [0]*(max(pt_y)+1)
    for i in pt_y:
        data_y[i]+=1
#--------------------Проверки критериев по y---------------------------------------------------------------------------
    chi_squared_uniform, critical_value_uniform, f_uniform = test_uniform(data_y,alpha)
    chi_squared_exponential, critical_value_exponential, f_exponential = test_exponential(data_y,alpha)
    ResShapiro = test_normal_Shapiro(data_y)
    ResDAgostino = test_normal_DAgostino(data_y)
    
    stats_value_y['iteration'].append(int((file.split('.')[0])[5:]))
    stats_value_y['alpha'].append(alpha)
    stats_value_y['Shapiro.stats'].append(ResShapiro.statistic)
    stats_value_y['Shapiro.p_value'].append(ResShapiro.pvalue)
    stats_value_y['DAgostino.stats'].append(ResDAgostino.statistic)
    stats_value_y['DAgostino.p_value'].append(ResDAgostino.pvalue)
    stats_value_y['Uniform.observable'].append(chi_squared_uniform)
    stats_value_y['Uniform.critical'].append(critical_value_uniform)
    stats_value_y['Exponential.observable'].append(chi_squared_exponential)
    stats_value_y['Exponential.critical'].append(critical_value_exponential)
    
    stats_work_y['iteration'].append(int((file.split('.')[0])[5:]))
    stats_work_y['Shapiro'].append(int((ResShapiro.pvalue != "D'Agostino not works!" and ResShapiro.pvalue > alpha)))
    stats_work_y['DAgostino'].append(int(ResDAgostino.pvalue != "D'Agostino not works!" and ResDAgostino.pvalue > alpha))
    stats_work_y['Uniform'].append(int(f_uniform))
    stats_work_y['Exponential'].append(int(f_exponential))
    

#--------------------Проверки критериев по x---------------------------------------------------------------------------
    chi_squared_uniform, critical_value_uniform, f = test_uniform(data_x)
    chi_squared_exponential, critical_value_exponential, f = test_exponential(data_x)
    ResShapiro = test_normal_Shapiro(data_x)
    ResDAgostino = test_normal_DAgostino(data_x)
    
    stats_value_x['iteration'].append(int((file.split('.')[0])[5:]))
    stats_value_x['alpha'].append(alpha)
    stats_value_x['Shapiro.stats'].append(ResShapiro.statistic)
    stats_value_x['Shapiro.p_value'].append(ResShapiro.pvalue)
    stats_value_x['DAgostino.stats'].append(ResDAgostino.statistic)
    stats_value_x['DAgostino.p_value'].append(ResDAgostino.pvalue)
    stats_value_x['Uniform.observable'].append(chi_squared_uniform)
    stats_value_x['Uniform.critical'].append(critical_value_uniform)
    stats_value_x['Exponential.observable'].append(chi_squared_exponential)
    stats_value_x['Exponential.critical'].append(critical_value_exponential)

    stats_work_x['iteration'].append(int((file.split('.')[0])[5:]))
    stats_work_x['Shapiro'].append(int((ResShapiro.pvalue != "D'Agostino not works!" and ResShapiro.pvalue > alpha)))
    stats_work_x['DAgostino'].append(int(ResDAgostino.pvalue != "D'Agostino not works!" and ResDAgostino.pvalue > alpha))
    stats_work_x['Uniform'].append(int(f_uniform))
    stats_work_x['Exponential'].append(int(f_exponential))
    
f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
alpha = float(f.readline())
category = int(f.readline())
max_iter = int(f.readline())
f.close()

path = ['Statistic\\log',
          f"Statistic\\log\\pole_{id_pole}",f"Statistic\\log\\pole_{id_pole}\\Points_{id_point}",
          f"Statistic\\log\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}",
          ]
for i in path:
    if not os.path.isdir(i):
        os.mkdir(i)

path_to_files = f"log\\pole_{id_pole}\\Points_{id_point}\\iter_{id_exp}"
onlyfiles = [f for f in os.listdir(path_to_files) if  os.path.isfile(os.path.join(path_to_files, f))] # получение всех файлов в папке
onlyfiles.sort(key=lambda x: int((x.split('.')[0])[5:]))
for filename in onlyfiles:
    programm(path_to_files, filename, category, alpha)

#---------------------------Выполнение критериев
            

df_val_crit_y : pd.DataFrame =  pd.DataFrame(stats_value_y)
df_work_crit_y : pd.DataFrame =  pd.DataFrame(stats_work_y)
df_val_crit_x : pd.DataFrame =  pd.DataFrame(stats_value_x)
df_work_crit_x : pd.DataFrame =  pd.DataFrame(stats_work_x)

#------------------------------Запись в excel
with pd.ExcelWriter(f"Statistic\\log\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\iter_{category}.xlsx") as writer:  
    df_val_crit_y.to_excel(writer, sheet_name='All_value_y')
    df_work_crit_y.to_excel(writer, sheet_name='is_work_y')
    df_val_crit_x.to_excel(writer, sheet_name='All_value_x')
    df_work_crit_x.to_excel(writer, sheet_name='is_work_x')
    
    