import scipy.stats as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json
import os

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

path_to_save = f"Statistic\\result\\depend_live_time_on_traps\\" 
create_path(path_to_save)

yinit_alive = {}
yinit_time_live = {}
f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
beg_trap = int(f.readline())
end_trap = int(f.readline())
beg_exp = int(f.readline())
end_exp = int(f.readline())
f.close()
df_orders = pd.read_excel(f'Statistic\\result\\depend_live_time_on_traps\\Function_{id_pole}.xlsx', index_col=0)

def mapping_einx_plus_b(values_x, a, b):
    return (2.71**values_x)*a + b                  # не работает на активных

def mapping_a_des_x_plus_b(values_x, a, b):
    return a/values_x + b                          # 33.171% на активных

def mapping_a_des_x_in_pow2_plus_b(values_x, a, b):
    return a/(values_x**2) + b                      # 12.015% на активных

def mapping_alogx_plus_b(values_x, a, b):
    return (np.log(values_x)*a + b)                # 66.715% на активных

def mapping_einx_plus_x_in_pow2(values_x, a, b):
    return ((2.71**values_x)*b + a*(values_x**2))  # не работает на активных

def mapping_poly2(values_x, a, b, c):
    return (c + (values_x)*b + a*(values_x**2))    # 146.078% на активных

def mapping_linear(values_x, a, b):
    return ((values_x)*a + b)                      # 93.767% на активных

def mapping_a_dels_sqrt_x_plus_b(values_x, a, b):
    return (a/(values_x**(1/2)) + b)               # 50.455% на активных

def mapping_a_dels_x_in_pow_b(values_x, a, b):
    return (a/(values_x**(b)))                     # 43.018% на активных

#----------------Аппроксимация по времени жизни------------------------------------
x_time_live = np.array([])
y_time_live = np.array([])
for i in range(len(df_orders['trapsCount'])):
    if(df_orders['CountData'][i] != 0):
        x_time_live = np.append(x_time_live,df_orders['trapsCount'][i])
        y_time_live = np.append(y_time_live,df_orders['mean_time_live'][i])
mem_time_live = {"Function":[], "a" : [], "b" : [], "c" : [], "Средняя ошибка" : []}
#---------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_des_x_plus_b,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
mem_time_live["Function"].append("$\\frac{a}{x} + b$")
mem_time_live["a"].append(a)
mem_time_live["b"].append(b)
mem_time_live["c"].append(None)

yinit_time_live["a/x + b"]=[]
for x in x_time_live:
    yinit_time_live["a/x + b"].append(mapping_a_des_x_plus_b(x,a,b))

so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yinit_time_live["a/x + b"][i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
mem_time_live["Средняя ошибка"].append(so)
#---------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_dels_sqrt_x_plus_b,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
mem_time_live["Function"].append("$\\frac{a}{\\sqrt{x}} + b$")
mem_time_live["a"].append(a)
mem_time_live["b"].append(b)
mem_time_live["c"].append(None)

yinit_time_live["a/sqrt(x) + b"]=[]
for x in x_time_live:
    yinit_time_live["a/sqrt(x) + b"].append(mapping_a_dels_sqrt_x_plus_b(x,a,b))

so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yinit_time_live["a/sqrt(x) + b"][i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
mem_time_live["Средняя ошибка"].append(so)

#--------------------------------------------------------------------------------------
# args, covar = curve_fit(mapping_a_des_x_in_pow2_plus_b,x_time_live,y_time_live)
# a =  args[0]
# b =  args[1]
# yinit_time_live["a/(x**2) + b"]=[]
# for x in x_time_live:
#     yinit_time_live["a/(x**2) + b"].append(mapping_a_des_x_in_pow2_plus_b(x,a,b))

# mem_time_live["Function"].append("$\\frac{a}{x^2} + b$")
# mem_time_live["a"].append(a)
# mem_time_live["b"].append(b)
# so = 0
# for i in range(len(y_time_live)):
#     if(y_time_live[i] !=0):
#         so += abs(yinit_time_live["a/(x**2) + b"][i]-y_time_live[i])/y_time_live[i]
# so = so / (len(y_time_live)) * 100
# so = round(so,3)
# mem_time_live["Средняя ошибка"].append(so)

#--------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_alogx_plus_b,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
yinit_time_live["a*log(x) + b"]=[]
for x in x_time_live:
    yinit_time_live["a*log(x) + b"].append(mapping_alogx_plus_b(x,a,b))

mem_time_live["Function"].append("$a \\ln{x} + b$")
mem_time_live["a"].append(a)
mem_time_live["b"].append(b)
mem_time_live["c"].append(None)

so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yinit_time_live["a*log(x) + b"][i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
mem_time_live["Средняя ошибка"].append(so)
#-------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_poly2,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
c =  args[2]
yinit_time_live["ax**2 + bx + c"]=[]
for x in x_time_live:
    yinit_time_live["ax**2 + bx + c"].append(mapping_poly2(x,a,b,c))

mem_time_live["Function"].append("$ax^2 + bx + c$")
mem_time_live["a"].append(a)
mem_time_live["b"].append(b)
mem_time_live["c"].append(c)
so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yinit_time_live["ax**2 + bx + c"][i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
mem_time_live["Средняя ошибка"].append(so)
#-------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_linear,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
#print(a,b)
yinit_time_live["ax + b"]=[]
for x in x_time_live:
    yinit_time_live["ax + b"].append(mapping_linear(x,a,b))

mem_time_live["Function"].append("$ax + b$")
mem_time_live["a"].append(a)
mem_time_live["b"].append(b)
mem_time_live["c"].append(None)

so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yinit_time_live["ax + b"][i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
mem_time_live["Средняя ошибка"].append(so)
#---------------------------------------------------------------------------------------
# args, covar = curve_fit(mapping_a_dels_x_in_pow_b,x_time_live,y_time_live)
# a =  args[0]
# b =  args[1]
# #print(a,b)
# yinit_time_live["a/(x**b)"]=[]
# for x in x_time_live:
#     yinit_time_live["a/(x**b)"].append(mapping_a_dels_x_in_pow_b(x,a,b))
# mem_time_live["Function"].append("$ax + b$")
# mem_time_live["a"].append(a)
# mem_time_live["b"].append(b)
# so = 0
# for i in range(len(y_time_live)):
#     if(y_time_live[i] !=0):
#         so += abs(yinit_time_live["ax + b"][i]-y_time_live[i])/y_time_live[i]
# so = so / (len(y_time_live)) * 100
# so = round(so,3)
# mem_time_live["Средняя ошибка"].append(so)

#-----------------------Рисуем картинки-----------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(x_time_live, y_time_live, marker='o', markersize=4, linewidth=3, label = "Истиные значения")
ax.plot(x_time_live, yinit_time_live["a*log(x) + b"], label = "$a \\ln{x}+ b$")
#ax.plot(x_time_live, yinit_time_live["a/(x**2) + b"], label = "$\\frac{a}{x^2} + b$")
#ax.plot(x_time_live, yinit_time_live["a/(x**b)"], label = "$\\frac{a}{x^b}$")
ax.plot(x_time_live, yinit_time_live["a/x + b"], label = "$\\frac{a}{x} + b$")
ax.plot(x_time_live, yinit_time_live["a/sqrt(x) + b"], label = "$\\frac{a}{\\sqrt{x}} + b$")
ax.plot(x_time_live, yinit_time_live["ax + b"], label = "$ax + b$")
ax.plot(x_time_live, yinit_time_live["ax**2 + bx + c"], label = "$ax^2+bx+c$")
ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Количество активных частиц') #Подпись для оси y
ax.legend()
plt.title('Зависимость количества активных частиц от количества ловушек') #Название
plt.savefig(path_to_save + f'Grafic_aproxy_all_function_time_live_{id_point}.png')
plt.show()
plt.close()

#----------------Аппроксимация по выжившим частицам------------------------------------
x_alive = df_orders['trapsCount']
y_alive = df_orders['mean_count_alive']
mem_alive = {"Function":[], "a" : [], "b" : [], "c" : [], "Средняя ошибка" : []}
#---------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_dels_sqrt_x_plus_b,x_alive,y_alive)
a =  args[0]
b =  args[1]
#print(a,b)
yinit_alive["a/sqrt(x) + b"]=[]
for x in x_alive:
    yinit_alive["a/sqrt(x) + b"].append(mapping_a_dels_sqrt_x_plus_b(x,a,b))

mem_alive["Function"].append("$\\frac{a}{\\sqrt{x}} + b$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)

so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["a/sqrt(x) + b"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)
#---------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_des_x_plus_b,x_alive,y_alive)
a =  args[0]
b =  args[1]
mem_alive["Function"].append("$\\frac{a}{x} + b$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)

yinit_alive["a/x + b"]=[]
for x in x_alive:
    yinit_alive["a/x + b"].append(mapping_a_des_x_plus_b(x,a,b))

so = 0
for i in range(len(yinit_alive["a/x + b"])):
    if(yinit_alive["a/x + b"][i] != 0):
        so += abs(yinit_alive["a/x + b"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)
#--------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_des_x_in_pow2_plus_b,x_alive,y_alive)
a =  args[0]
b =  args[1]
yinit_alive["a/(x**2) + b"]=[]
for x in x_alive:
    yinit_alive["a/(x**2) + b"].append(mapping_a_des_x_in_pow2_plus_b(x,a,b))

mem_alive["Function"].append("$\\frac{a}{x^2} + b$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)
so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["a/(x**2) + b"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)

#--------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_alogx_plus_b,x_alive,y_alive)
a =  args[0]
b =  args[1]
yinit_alive["a*log(x) + b"]=[]
for x in x_alive:
    yinit_alive["a*log(x) + b"].append(mapping_alogx_plus_b(x,a,b))

mem_alive["Function"].append("$a\\ln{x} + b$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)
so = 0
for i in range(len(yinit_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["a*log(x) + b"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)
#-------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_poly2,x_alive,y_alive)
a =  args[0]
b =  args[1]
c =  args[2]
yinit_alive["ax**2 + bx + c"]=[]
for x in x_alive:
    yinit_alive["ax**2 + bx + c"].append(mapping_poly2(x,a,b,c))

mem_alive["Function"].append("$ax^2 + bx + c$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(c)
so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["ax**2 + bx + c"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)
#-------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_linear,x_alive,y_alive)
a =  args[0]
b =  args[1]
#print(a,b)
yinit_alive["ax + b"]=[]
for x in x_alive:
    yinit_alive["ax + b"].append(mapping_linear(x,a,b))

mem_alive["Function"].append("$ax + b$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)

so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["ax + b"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)
#---------------------------------------------------------------------------------------
args, covar = curve_fit(mapping_a_dels_x_in_pow_b,x_alive,y_alive)
a =  args[0]
b =  args[1]
#print(a,b)
yinit_alive["a/(x**b)"]=[]
for x in x_alive:
    yinit_alive["a/(x**b)"].append(mapping_a_dels_x_in_pow_b(x,a,b))

mem_alive["Function"].append("$\\frac{a}{x^b}$")
mem_alive["a"].append(a)
mem_alive["b"].append(b)
mem_alive["c"].append(None)

so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yinit_alive["a/(x**b)"][i]-y_alive[i])/y_alive[i]
so = so / (len(y_alive)) * 100
so = round(so,3)
mem_alive["Средняя ошибка"].append(so)

#-----------------------Рисуем картинки-----------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(x_alive, y_alive, marker='o', markersize=4,linewidth=3, label = "Истиные значения")
ax.plot(x_alive, yinit_alive["a*log(x) + b"], label = "$a \\ln{x}+ b$")
ax.plot(x_alive, yinit_alive["a/(x**2) + b"], label = "$\\frac{a}{x^2} + b$")
ax.plot(x_alive, yinit_alive["a/(x**b)"], label = "$\\frac{a}{x^b}$")
ax.plot(x_alive, yinit_alive["a/sqrt(x) + b"], label = "$\\frac{a}{\\sqrt{x}} + b$")
ax.plot(x_alive, yinit_alive["ax + b"], label = "$ax + b$")
ax.plot(x_alive, yinit_alive["ax**2 + bx + c"], label = "$ax^2+bx+c$")

ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Количество активных частиц') #Подпись для оси y
ax.legend()
plt.title('Зависимость количества активных частиц от количества ловушек') #Название
plt.savefig(path_to_save + f'Grafic__aproxy_all_function_alive_{id_point}.png')
plt.show()
plt.close()

#------------------------------Запись в excel
df_alive : pd.DataFrame =  pd.DataFrame(mem_alive)
df_time_live : pd.DataFrame =  pd.DataFrame(mem_time_live)

with pd.ExcelWriter(path_to_save + f"Function_alroxy_{id_point}.xlsx") as writer:  
    df_alive.to_excel(writer, sheet_name='alive')
    df_time_live.to_excel(writer, sheet_name='time live')
