from scipy.stats import mean
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
        "time_live" : []
        }
cnt_trap : int = 0
def Get_data(id_pole : int , id_point : int, id_traps : int, exp_id : int, arr : list(int)):
    # открытие файла
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\Statist_{exp_id}.txt"
    print(path)
    F = open(path,'r+')
    data :str = F.readline()
    print(data)
    templates : json = json.loads(data)
    F.close()
    if(templates["Live_time"] < 0):
        return
    arr.append(templates["Live_time"])
    global cnt_trap
    cnt_trap = templates["trapsCount"]
    
#f = open('Statistic\\config.txt', 'r+')
id_pole = 0
id_point = 0
#f.close()

for id_traps in range(131):
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\"
    arr = []
    for exp_id in range(2,23):
        Get_data(id_pole, id_point, id_traps, exp_id, arr)
    mem_to_exel["trap_id"].append(id_traps)
    mem_to_exel["trapsCount"].append(cnt_traps)
    mem_to_exel["mean_time_live"].append(arr.mean())

path_to_save = f"Statistic\\result\\depend_live_time_on_traps\\" 
create_path(path_to_save)
#-----------------------Рисуем картинки-----------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(mem_to_exel["trapsCount"], mem_to_exel["mean_time_live"], marker='o', markersize=4)
ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Колличество ловушек') #Подпись для оси х
plt.ylabel('Время жизни') #Подпись для оси y
plt.title('Зависимость времени жизни от ловушек при $3 * 10^6$ итераций') #Название
plt.savefig(path_to_save + f'Grafic_{id_exp}.png')
plt.show()
plt.close()

#------------------------------Запись в excel
df_x : pd.DataFrame =  pd.DataFrame(mem_to_exel)
df_x : pd.DataFrame =  pd.DataFrame(mem_to_exel_out_null)

with pd.ExcelWriter(path_to_save + f"Function_{id_point}.xlsx") as writer:  
    df_x.to_excel(writer, sheet_name='Data_all')
    df_x.to_excel(writer, sheet_name='Data_out_NULL')