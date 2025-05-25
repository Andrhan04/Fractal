import pandas as pd
import matplotlib.pyplot as plt
import os

# pip install pandas xlsxwriter openpyxl faker 
# код для проверки критериев о распределении по итерациям

#----------------------------------------------------------------------------------------------------------------
# Память
all_cnt_x = dict()
all_cnt_y = dict()

#----------------------------------------------------------------------------------------------------------------
def programm(path : str, file : str, step : int, path_to_save : str, max_x : int, max_y : int):
    # открытие файла
    F = open(path + '/' + file,'r+')
    data = []
    data = F.readlines()
    F.close()
    # обработка данных
    data_x = [0]*(max_x//step + 1)
    data_y = [0]*(max_y//step + 1)
    for s in data:
        buf = s.split()
        data_x[min(int(float(buf[0]))//step,max_x//step)] += 1
        data_y[min(int(float(buf[1]))//step,max_y//step)] += 1
#-------------------------------------------------------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.xlabel('Категории')
    plt.ylabel('Значения')
    plt.title('Гистограмма данных из файла')
    plt.ylim(0, 200)
    plt.bar(range(len(data_x)), data_x, color='blue', alpha=0.7, align='edge', linewidth = 0, width = 1)
    #plt.plot(range(len(data_x)), data_x, color='green', marker='o', markersize=0.01)
    plt.savefig(path_to_save + '/x/' + (file.split('.'))[0] + '.png')
    plt.close()
#-------------------------------------------------------------------------------------------------------------
    plt.figure(figsize=(8, 5))
    plt.ylim(0,200)
    plt.xlabel('Категории')
    plt.ylabel('Значения')
    plt.title('Гистограмма данных из файла')
    plt.bar(range(len(data_y)), data_y, color='blue', alpha=0.7)
    #plt.plot(range(len(data_y)), data_y, color='green', marker='o', markersize=0.01)
    plt.savefig(path_to_save + '/y/' + (file.split('.'))[0] + '.png')
    plt.close()
#----------------Запись результатов в память-------------------------------------------------------------------------------
    all_cnt_x[file] = data_x
    all_cnt_y[file] = data_y
    
    
f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
category = int(f.readline())
max_x : int = int(f.readline())
max_y : int = int(f.readline())
step : int = int(f.readline())
f.close()

path = ['Statistic\\hist',
          f"Statistic\\hist\\pole_{id_pole}",f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}",
          f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}",
          f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}",
          f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\x",
          f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\y",
          ]
for i in path:
    if not os.path.isdir(i):
        os.mkdir(i)

path_to_files = f"log\\pole_{id_pole}\\Points_{id_point}\\iter_{id_exp}"
onlyfiles = [f for f in os.listdir(path_to_files) if  os.path.isfile(os.path.join(path_to_files, f))] # получение всех файлов в папке
onlyfiles.sort(key=lambda x: int((x.split('.')[0])[5:]))
i : int = 0
n : int = len(onlyfiles)
for filename in onlyfiles:
    i += 1
    if(i % (n//100) == 0):
        print(f'Complete {i // (n//100)}%')
    if (int((filename.split('.'))[0][5:]) % step == 0 and int((filename.split('.'))[0][5:]) != 0):
        programm(path_to_files, filename, category, path_to_save=f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}", max_x = max_x , max_y = max_y)


#---------------------------Выполнение критериев
            

df_x : pd.DataFrame =  pd.DataFrame(all_cnt_x)
df_y : pd.DataFrame =  pd.DataFrame(all_cnt_y)

#------------------------------Запись в excel
with pd.ExcelWriter(f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\distribution_{category}.xlsx") as writer:  
    df_x.to_excel(writer, sheet_name='count_x')
    df_y.to_excel(writer, sheet_name='count_y')
    
    