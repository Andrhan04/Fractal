import pandas as pd
import numpy as np
import json
import os

def get_data(id_pole : int , id_point : int, id_traps : int, exp_id : int):
    path = f"log_whith_traps\\pole_{id_pole}\\Points_{id_point}\\Traps_{id_traps}\\dead_{exp_id}.txt"
    iter : list = np.array([])
    x : list = np.array([])
    y : list = np.array([])
    file = open(path,'r+')
    buf = file.readlines()
    file.close()
    cnt = 0
    for curr in buf:
        s = curr.split()
        iter = np.append(iter,s[0])
        x = np.append(x, s[1])
        y = np.append(y, s[2])
        cnt += 1
        if(cnt >= 700):
            break
    return np.mean(iter), np.mean(x), np.mean(y)

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)

mem_to_exp = {  "trap_id" : [], 
                "trapsCount" : [], 
                "mean_iter" : [],
                "median_iter" : [],
                "mean_x" : [],
                "median_x" : [],
                "mean_y" : [],
                "median_y" : []
            }   

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
    data = {"iter" : [], "x" : [], "y" : []}
    for id_exp in range(beg_exp, end_exp):
        mem = []
        mem = get_data(id_pole,id_point, id_trap, id_exp)
        data["iter"].append(mem[0])
        data["x"].append(mem[1])
        data["y"].append(mem[2])
    mem_to_exp["trap_id"].append(id_trap)
    mem_to_exp["trapsCount"].append(trap_cnt)
    mem_to_exp["mean_iter"].append(np.mean(data["iter"]))
    mem_to_exp["median_iter"].append(np.median(data["iter"]))
    mem_to_exp["mean_x"].append(np.mean(data["x"]))
    mem_to_exp["median_x"].append(np.median(data["x"]))
    mem_to_exp["mean_y"].append(np.mean(data["y"]))
    mem_to_exp["median_y"].append(np.median(data["y"]))

df_x : pd.DataFrame =  pd.DataFrame(mem_to_exp)
path_to_save = f"log\\my_find"
create_path(path_to_save)
with pd.ExcelWriter(path_to_save + f"Function_{id_pole}.xlsx") as writer:  
    df_x.to_excel(writer, sheet_name='Data_all')