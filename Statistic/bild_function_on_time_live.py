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
        "trap_cnt" : [], 
        "time_live" : []
        }

mem = []

def Get_data(path : str, exp_id : int):
    # открытие файла
    file = f"Statist_{exp_id}.txt"
    print(path)
    F = open(path + file,'r+')
    data :str = F.readline()
    print(data)
    templates : json = json.loads(data)
    F.close()
    # if(templates["Live_time"] < 0):
    #     return
    mem_to_exel["trap_id"].append(templates["trap_id"])
    mem_to_exel["trap_cnt"].append(templates["trapsCount"])
    mem_to_exel["time_live"].append(templates["Live_time"])
    mem.append([templates["trapsCount"], templates["Live_time"]])
    
#f = open('Statistic\\config.txt', 'r+')
id_pole = 0
id_point = 0
id_exp = 1
#f.close()
for id_traps in range(132):
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\"
    Get_data(path, id_exp)

path_to_save = f"Statistic\\log_func\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\" 
create_path(path_to_save)
plt.plot(mem_to_exel["trap_cnt"], mem_to_exel["time_live"], marker='o', markersize=4)
plt.xlabel('Колличество ловушек') #Подпись для оси х
plt.ylabel('Время жизни') #Подпись для оси y
plt.title('Зависимость времени жизни от ловушек при $10^6$ итераций') #Название
plt.savefig(path_to_save + f'Grafic_{id_exp}.png')
plt.show()

df_x : pd.DataFrame =  pd.DataFrame(mem)
#------------------------------Запись в excel
with pd.ExcelWriter(path_to_save + f"Function_{id_exp}.xlsx") as writer:  
    df_x.to_excel(writer, sheet_name='Data')