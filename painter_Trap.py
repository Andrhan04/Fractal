import matplotlib.pyplot as plt

id_trap = 501
id_pole = 5
id_point = 0
id_exp = 2

#       Ловушки
# чтение из файла
F = open("Sowing\\Trap_slow\\Traps_" + str(id_trap) + ".txt",'r+')
data = []
sz = int(F.readline())
data = F.readlines()
F.close()
tr_x = []
tr_y = []
i = 0
for s in data:
    buf = s.split()
    tr_x.append(float(buf[0]))
    tr_y.append(float(buf[1]))
    i += 1

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
# F = open("log\\pole_" + str(id_pole) + "\\Points_" + str(id_point) + "\\Alive_" + str(id_exp) + ".txt",'r+')
data = []
# data = F.readlines()
# F.close()
# обработка данных
pt_x = []
pt_y = []
for s in data:
    buf = s.split()
    pt_x.append((float(buf[0])))
    pt_y.append((float(buf[1])))

plt.figure()
plt.plot(fractal_x, fractal_y, label = "Фрактал")
plt.scatter(tr_x, tr_y, color = 'g', label='Частицы')
plt.scatter(pt_x, pt_y, color = 'r', label='Частицы', s = 1)
plt.show()