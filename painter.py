import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import os
id_trap = 0
id_pole = 4
id_point = 1
id_exp = 4
# Поле
F = open("Sowing\\Fractal_convecs\\koch_curve_pore_" + str(id_pole) + ".txt",'r+')
data = []
data = F.readlines()
F.close()
fractal_x = []
fractal_y = []


for s in data:
    buf = s.split()
    fractal_x.append(float(buf[0]))
    fractal_y.append(float(buf[1]))
fractal_x.append(fractal_x[0])
fractal_y.append(fractal_y[1])

#       Частицы
# чтение из файла
#F = open(f"log\\pole_{id_pole}\\Points_{id_point}\\iter_{id_exp}\\iter_1000.txt",'r+')
F = open(f"log\\pole_{id_pole}\\Points_{id_point}\\Alive_{id_exp}.txt",'r+')
data = []
data = F.readlines()
F.close()
# обработка данных
pt_x = []
pt_y = []
for s in data:
    buf = s.split()
    pt_x.append((float(buf[0])))
    pt_y.append((float(buf[1])))

buf_x = [100,   0,  0,  100] 
buf_y = [450, 450, 550, 550]

path = ['images',
          f"images\\Fractal_{id_pole}",
          f"images\\Fractal_{id_pole}\\point_{id_point}"
          ]
for i in path:
    if not os.path.isdir(i):
        os.mkdir(i)

plt.figure()
plt.plot(fractal_x, fractal_y, label = "Фрактал")
plt.plot(buf_x, buf_y, label = "Фрактал", color = 'r')
plt.scatter(pt_x, pt_y, color = 'r', label='Частицы', s = 1)
plt.savefig(f"images\\Fractal_{id_pole}\\point_{id_point}\\Alive_{id_exp}.png")
plt.show()