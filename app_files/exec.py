import numpy as np
import PIL
import os
import matplotlib.pyplot as plt
import torch


from centerfinder import *
from seq_finder import *
from preprocess import *
from pizzacutter import *
from stats import *
from ui import *
# Initialising program

cell_array = []
cluster_array = []

raw_images = []

IMG_SAVE_PATH_TEST, CONT_SET = get_file()

for directory in os.listdir(IMG_SAVE_PATH_TEST):
  path = os.path.join(directory, IMG_SAVE_PATH_TEST)
  if os.path.isdir(path) == True:
    for image in os.listdir(path):
      new_path = os.path.join(path, image)
      try:
          imgpath = PIL.Image.open(new_path)
          # print(imgpath)
          imgpath = imgpath.convert('RGB')
          img = np.asarray(imgpath)
          raw_images.append([img, directory])
      except PIL.UnidentifiedImageError:
          print('error: skipped image')

if CONT_SET == 'high':
    edges = preprocess_image_high_cont(img)

else:
    edges = preprocess_image_low_cont(img)
masks = generate_mask(edges, init_mask_gen)
show_mask(img, masks)
cell_array, cluster_array = separate_clusters(masks, img)

temp = process_cluster(cluster_array)

cell_array += temp

# print('Array of individual cells...')
# for cell in cell_array:
#     plt.imshow(cell)
#     plt.show()

cats, err_cnt = stats(cell_array)
fetch_stats(cats, err_cnt)





