import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

# 2. Проверка на равномерное распределение
def test_uniform(data, alpha = 0.01):
    # Определение диапазона данных
    min_val, max_val = np.min(data), np.max(data)
    bins = np.linspace(min_val, max_val, 6)  # 5 интервалов для равномерного распределения
    observed_freq, _ = np.histogram(data, bins=bins)
    
    # Теоретические частоты для равномерного распределения
    expected_freq = len(data) / len(observed_freq) * np.ones_like(observed_freq)

    # Вычисляем значение критерия χ²
    chi_squared = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
    
    # Степени свободы
    df = len(observed_freq) - 1
    critical_value = stats.chi2.ppf(1 - alpha, df)
    
    print(f'Равномерное распределение: χ² = {chi_squared:.4f}, критическое значение = {critical_value:.4f}')
    if(chi_squared > critical_value):
        print('гипотеза отклоняется')
    else:
        print('нет оснований отвергать гипотезу ')
    return chi_squared, critical_value, chi_squared > critical_value


id_trap = 0
id_pole = 0
id_point = 0
id_exp = 0
name = "Fractal_2_exp_4.png"

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
F = open(f"log\\pole_{id_pole}\\Points_{id_point}\\iter_{id_exp}\\iter_1000.txt",'r+')
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

plt.figure()
plt.plot(fractal_x, fractal_y, label = "Фрактал")
plt.plot(buf_x, buf_y, label = "Фрактал", color = 'r')
plt.scatter(pt_x, pt_y, color = 'r', label='Частицы', s = 1)
plt.show()