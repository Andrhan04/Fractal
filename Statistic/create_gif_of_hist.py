import imageio.v2 as imageio
import os

# pip install imageio

f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
category = int(f.readline())
max_x : int = int(f.readline())
max_y : int = int(f.readline())
step : int = int(f.readline())
f.close()

path_to_files = f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\x"
images = [f for f in os.listdir(path_to_files) if  os.path.isfile(os.path.join(path_to_files, f))]  # Список изображений
images = images[1:]
images.sort(key=lambda x: int((x.split('.')[0])[5:]))
with imageio.get_writer(f'Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\animation_x.gif', mode='I') as writer:
    for img in images:
        if ((img.split('_')[0] == "Alive") or (int((img.split('.'))[0][5:]) % step == 0 and ((img.split('.'))[0][5:]) != 0)):
            writer.append_data(imageio.imread(path_to_files + "\\" + img))  # Добавление каждого изображения в отдельности
            
path_to_files = f"Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\y"
images = [f for f in os.listdir(path_to_files) if  os.path.isfile(os.path.join(path_to_files, f))]  # Список изображений
images = images[1:]
images.sort(key=lambda x: int((x.split('.')[0])[5:]))
with imageio.get_writer(f'Statistic\\hist\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\category_{category}\\animation_y.gif', mode='I') as writer:
    for img in images:
        if ((img.split('_')[0] == "Alive") or (int((img.split('.'))[0][5:]) % step == 0 and ((img.split('.'))[0][5:]) != 0)):
            writer.append_data(imageio.imread(path_to_files + "\\" + img))  # Добавление каждого изображения в отдельности