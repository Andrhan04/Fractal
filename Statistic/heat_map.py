import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from os import listdir
import os
from os.path import isfile, join

# Нужно изменить path_to_fractale path_files new_folder

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)


f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
f.close()

fractal_x = []
fractal_y = []
path_to_fractale = f'Sowing\\Fractal_convecs\\koch_curve_pore_{id_pole}.txt' # путь до файла фигуры (координаты вершины)
with open(path_to_fractale) as f:
    for line in f:
        arr = line.split()
        if(len(arr)):
            fractal_x.append(float(arr[0]))
            fractal_y.append(float(arr[1]))
fractal_x.append(fractal_x[0])
fractal_y.append(fractal_y[0])

path_files = f"log\\pole_{id_pole}\\Points_{id_point}\\iter_{id_exp}" # Путь до папки с файлами расположении частиц
new_folder = f"Statistic\\heap_map\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}" # Путь до новой папки
create_path(new_folder)

onlyfiles = [f for f in listdir(path_files) if isfile(join(path_files, f))] # получение всех файлов в папке
n : int = len(onlyfiles)
i : int = 0
for path_to_file in onlyfiles:
    i += 1
    if(i%(n//100) == 0):
        print(f"Complete {i//(n//100)} %")
    F = open(path_files + '\\' + path_to_file)
    data = []
    data = F.readlines()
    F.close()
    x = []
    y = []
    for s in data:
        buf = s.split()
        x.append((float(buf[0])))
        y.append((float(buf[1])))
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)

    plt.plot(fractal_x, fractal_y, label = "Фрактал")
    plt.scatter(x, y, c=z,  s=1)
    path_to_file = path_to_file.replace('.txt','')
    plt.savefig(new_folder+ "\\" + path_to_file + ".png")
    plt.cla()