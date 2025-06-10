import pandas as pd
import numpy as np
import json
import os

def get_data(id_pole : int , id_point : int, id_traps : int, exp_id : int):
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\dead_{exp_id}.txt"
    iter : list = np.array([])
    x : list = np.array([])
    y : list = np.array([])
    try:
        file = open(path,'r+')
        buf = file.readlines()
        file.close()
    except:
        print(f"No file dead_{exp_id}")
        return [],[],[]
    cnt = 0
    for curr in buf:
        s = curr.split()
        iter = np.append(iter, int(s[0]))
        x = np.append(x, float(s[1]))
        y = np.append(y, float(s[2]))
        cnt += 1
        if(cnt >= 700):
            break
    return iter, x, y

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

mem_to_exel = { "pole_4" : {"trapsCount" : [],"x" : [], "y" : []}}
f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
beg_trap = int(f.readline())
end_trap = int(f.readline())
beg_exp = int(f.readline())
end_exp = int(f.readline())
f.close()

for id_trap in range(beg_trap, end_trap):
    file = open(f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_trap}\\Statist_{beg_exp}.txt",'r+')
    data :str = file.readline()
    templates : json = json.loads(data)
    trap_cnt = templates["trapsCount"]
    file.close()
    mem = {
            "iter" : [], 
            "x" : [], 
            "y" : []
        }
    for id_exp in range(beg_exp, end_exp):
        iter, x, y = get_data(id_pole,id_point, id_trap, id_exp)
        if(len(iter) != 0):
            mem["iter"] = np.append(mem["iter"],iter)
            mem["x"] = np.append(mem["x"],x)
            mem["y"] = np.append(mem["y"],y)
    mem_to_exel[trap_cnt] = mem
    mem_to_exel["pole_4"]["trapsCount"] = np.append(mem_to_exel["pole_4"]["trapsCount"], trap_cnt)
    mem_to_exel["pole_4"]["x"] = np.append(mem_to_exel["pole_4"]["x"],np.mean(mem["x"]))
    mem_to_exel["pole_4"]["y"] = np.append(mem_to_exel["pole_4"]["y"],np.mean(mem["y"]))
    

path_to_save = f"Statistic\\result\\my_find\\"
create_path(path_to_save)
with pd.ExcelWriter(path_to_save + f"pole_{id_pole}.xlsx") as writer:  
    for i in mem_to_exel:
        df_x : pd.DataFrame = pd.DataFrame(mem_to_exel[i])
        df_x.to_excel(writer, sheet_name=str(i))