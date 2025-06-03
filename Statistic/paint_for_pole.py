import pandas as pd
import matplotlib.pyplot as plt
import os

def create_path (all_path : str):
    path = all_path.split('\\')
    curr_path : str = ""
    for i in path:
        curr_path += i + "\\"
        if not os.path.isdir(curr_path):
            os.mkdir(curr_path)
            
path_to_save : str = f"Statistic\\result\\differ_pole\\" 
create_path(path_to_save)

f = open('Statistic\\config.txt', 'r+')
id_pole_str = int(f.readline())
id_pole_end = int(f.readline())
f.close()
fig, ax = plt.subplots()

for id_pole in range(id_pole_str, id_pole_end + 1):
    try:
        df_orders = pd.read_excel(f'Statistic\\result\\depend_live_time_on_traps\\Function_{id_pole}.xlsx', index_col=0)
        x_time_live = df_orders['trapsCount']
        y_time_live = df_orders['mean_time_live']
        ax.plot(x_time_live, y_time_live, label = f"Фрактал {id_pole}")
        print(f"add {id_pole}")
    except Exception as e:
        print("No file")
        print(e)

ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Время жизни') #Подпись для оси y
ax.legend()
plt.title('Зависимость количества активных частиц от количества ловушек') #Название
plt.savefig(path_to_save + f'Grafic_time_live.png')
plt.show()
plt.close(fig)

fig, ax = plt.subplots()
for id_pole in range(id_pole_str, id_pole_end + 1):
    try:
        df_orders = pd.read_excel(f'Statistic\\result\\depend_live_time_on_traps\\Function_{id_pole}.xlsx', index_col=0)
        x_alive = df_orders['trapsCount']
        y_alive = df_orders['mean_count_alive']
        ax.plot(x_alive, y_alive, label = f"Фрактал {id_pole}")
    except Exception as e:
        print(f"No file {id_pole}")
ax.grid(True, linestyle='-.', linewidth=0.5, color='gray')
ax.tick_params(axis='both', which='both', labelsize=8, width=1, color='red')
plt.xlabel('Количество ловушек') #Подпись для оси х
plt.ylabel('Количество активных частиц') #Подпись для оси y
ax.legend()
plt.title('Зависимость количества активных частиц от количества ловушек') #Название
plt.savefig(path_to_save + f'Grafic_alive.png')
plt.show()
plt.close()