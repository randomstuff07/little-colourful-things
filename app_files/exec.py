import numpy as np
import PIL
import os
import flet
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

cats = []
err_cnt = np.zeros(7)
page = ft.Page
page.padding = 40
pb = ft.ProgressBar(width=400)
page.add(
    Row(
        [Text('Processing the images...')]
    ),
    ft.Column([ ft.Text("Doing something..."), pb]),
)
for i, img in enumerate(raw_images):
    
    pb.value = (i/len)
    page.update()
    if pb.value == 1:
        page.visible = False
        
    if CONT_SET == 'high':
        edges = preprocess_image_high_cont(img)
    else:
        edges = preprocess_image_low_cont(img)

    masks = generate_mask(edges, init_mask_gen)
    show_mask(img, masks)
    cell_array, cluster_array = separate_clusters(masks, img)

    temp = process_cluster(cluster_array)

    cell_array += temp
    cats_temp, err_cnt_temp = stats(cell_array)
    cats = cats_temp
    err_cnt += err_cnt_temp
# print('Array of individual cells...')
# for cell in cell_array:
#     plt.imshow(cell)
#     plt.show()

fetch_stats(cats, err_cnt)





