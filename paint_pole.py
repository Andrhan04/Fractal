import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import os
import seaborn as sns

id_pole = 0

# Поле
F = open("Sowing\\Fractal_convecs\\koch_curve_pore_" + str(id_pole) + ".txt",'r+')
data = []
data = F.readlines()
F.close()
fractal_x = []
fractal_y = []
buf_x = [100,   0,  0,  100] 
buf_y = [450, 450, 550, 550]
for s in data:
    buf = s.split()
    fractal_x.append(float(buf[0]))
    fractal_y.append(float(buf[1]))
fractal_x.append(fractal_x[0])
fractal_y.append(fractal_y[1])

# создание пути к папке
path = ['images', "images\\color", "images\\black"]
for i in path:
    if not os.path.isdir(i):
        os.mkdir(i)
        
# Отрисовка поля
# Цветное
plt.figure()
plt.xlabel("Длина интервала", size= 11)
plt.ylabel("Количество интервалов", size= 11)
plt.plot(fractal_x, fractal_y, label = "Фрактал")
plt.plot(buf_x, buf_y, label = "Фрактал", color = 'r')
plt.savefig(f"images\\color\\Fractal_{id_pole}.png")
plt.show()
plt.close()

# Черно-белое
# plt.figure()
#sns.lineplot(x=fractal_x, y=fractal_y, color="black")
fig, axes = plt.subplots(figsize=(7, 7))
axes.set_xlabel('X Axis', size = 11)
axes.set_ylabel('Y Axis', size = 11)
axes.plot(fractal_x, fractal_y, label = "Фрактал", color = 'black')
axes.plot(buf_x, buf_y, label = "Фрактал", color = 'black')
fig.savefig(f"images\\black\\Fractal_{id_pole}.png")
fig.show()