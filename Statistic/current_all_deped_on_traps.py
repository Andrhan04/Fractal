import scipy.stats as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

mem_to_exel = { "trap_id" : [], 
        "trapsCount" : [], 
        "mean_time_live" : [],
        "mean_count_alive" : [],
        "CountData" : []
        }
cnt_trap : int = 0
def Get_data(id_pole : int , id_point : int, id_traps : int, exp_id : int, liveTime : list, alive : list):
    # открытие файла
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\Statist_{exp_id}.txt"
    print(path)
    F = open(path,'r+')
    data :str = F.readline()
    print(data)
    templates : json = json.loads(data)
    F.close()
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\Alive_{exp_id}.txt"
    F = open(path,'r+')
    data = F.readlines()
    F.close()
    alive.append(len(data))
    global cnt_trap
    cnt_trap = templates["trapsCount"]
    if(templates["Live_time"] < 0):
        return
    liveTime.append(templates["Live_time"])
    
    
#f = open('Statistic\\config.txt', 'r+')
id_pole = 0
id_point = 0
#f.close()

for id_traps in range(151):
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\"
    arr_time_live = []
    arr_cnt_alive = []
    for exp_id in range(2,23):
        Get_data(id_pole, id_point, id_traps, exp_id, arr_time_live, arr_cnt_alive)
    mem_to_exel["trap_id"].append(id_traps)
    mem_to_exel["trapsCount"].append(cnt_trap)
    mem_to_exel["CountData"].append(len(arr_time_live))
    mem_to_exel["mean_count_alive"].append(sns.gmean(arr_cnt_alive))
    if(arr_time_live != []):
        mem_to_exel["mean_time_live"].append(sns.gmean(arr_time_live))
    else:
        mem_to_exel["mean_time_live"].append(None)

path_to_save = f"Statistic\\result\\depend_live_time_on_traps\\" 
create_path(path_to_save)
#-----------------------Рисуем картинки-----------------------------------------------------------------
#-----------------------time live------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(mem_to_exel["trapsCount"], mem_to_exel["mean_time_live"], marker='o', markersize=4)
ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Время жизни') #Подпись для оси y
plt.title('Зависимость времени жизни от ловушек при $3 * 10^6$ итераций') #Название
plt.savefig(path_to_save + f'Grafic_time_live_{id_point}.png')
plt.show()
plt.close()
#------------------------Alive----------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(mem_to_exel["trapsCount"], mem_to_exel["mean_count_alive"], marker='o', markersize=4)
ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Количество активных частиц') #Подпись для оси y
plt.title('Зависимость количества активных частиц от количества ловушек \nпри $3 * 10^6$ итераций') #Название
plt.savefig(path_to_save + f'Grafic_alive_{id_point}.png')
plt.show()
plt.close()

#------------------------------Запись в excel
df_x : pd.DataFrame =  pd.DataFrame(mem_to_exel)

with pd.ExcelWriter(path_to_save + f"Function_{id_point}.xlsx") as writer:  
    df_x.to_excel(writer, sheet_name='Data_all')