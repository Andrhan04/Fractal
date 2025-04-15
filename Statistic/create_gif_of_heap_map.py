import imageio.v2 as imageio
import os

# pip install imageio

f = open('Statistic\\config.txt', 'r+')
id_pole = int(f.readline())
id_point = int(f.readline())
id_exp = int(f.readline())
f.close()

path_to_files = f"Statistic\\heap_map\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}"
images = [f for f in os.listdir(path_to_files) if  os.path.isfile(os.path.join(path_to_files, f))]  # Список изображений
images.sort(key=lambda x: int((x.split('.')[0])[5:]))
with imageio.get_writer(f'Statistic\\heap_map\\pole_{id_pole}\\Points_{id_point}\\exp_{id_exp}\\animation.gif', mode='I') as writer:
    for img in images:
        writer.append_data(imageio.imread(path_to_files + "\\" + img))  # Добавление каждого изображения в отдельности