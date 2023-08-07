from init import *

WORKING_DIR = '/Users/aaditmahajan/Documents/Summer_Internship/app_files'
init(WORKING_DIR)

import numpy as np
import cv2
import PIL
import math
import imutils
import os
import matplotlib.pyplot as plt
import random

from centerfinder import *
from seq_finder import *
from preprocess import *
from pizzacutter import *

'''
Initialising program
Installing dependencies
'''

cell_array = []
cluster_array = []
curr_path = os.getcwd()

IMG_SAVE_PATH_TEST = os.path.join(curr_path, "dataset/Picture_4.jpg")
input_image = PIL.Image.open(IMG_SAVE_PATH_TEST)
input_image = input_image.convert('RGB')
img = np.asarray(input_image, dtype='uint8')

# for directory in os.listdir(IMG_SAVE_PATH_TEST):
#   path = os.path.join(directory, IMG_SAVE_PATH_TEST)
#   if os.path.isdir(path) == True:
#     for image in os.listdir(path):
#       new_path = os.path.join(path, image)
#       try:
#           imgpath = PIL.Image.open(new_path)
#           # print(imgpath)
#           imgpath = imgpath.convert('RGB')
#           img = np.asarray(imgpath)
#           raw_images.append([img, directory])
#       except PIL.UnidentifiedImageError:
#           print('error: skipped image')

edges = preprocess_image(img)

masks = generate_mask(edges, init_mask_gen)
show_mask(img, masks)
cell_array, cluster_array = separate_clusters(masks, img)

temp = process_cluster(cluster_array)
cell_array = np.concatenate((cell_array, temp))
print('Array of individual cells...')
for cell in cell_array:
    plt.imshow(cell)
    plt.show()

'''
Below this part is the execution of the error_type classification
'''

image = cell_array[0]
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

spores_red = red_spores(image)
spores_blue = blue_spores(image)
spores_pink = pink_spores(image)

plt.subplot(1, 3, 1)
plt.imshow(spores_red)
plt.title('Red Spores')
plt.subplot(1, 3, 2)
plt.imshow(spores_blue)
plt.title('Blue Spores')
plt.subplot(1, 3, 3)
plt.imshow(spores_pink)
plt.title('Pink Spores')
plt.show()

spores = spores_red+spores_pink+spores_blue
spgray = cv2.cvtColor(spores, cv2.COLOR_BGR2GRAY)

print('RED MASKS: ')
red_centers = find_centers(spores_red, spores)
print('Red spore center positions: ', red_centers)
print('----------------------------------------------------------------')
print('BLUE MASKS: ')
blue_centers = find_centers(spores_blue, spores)
print('Blue spore center positions: ', blue_centers)
print('----------------------------------------------------------------')
print('PINK_MASKS: ')
pink_centers = find_centers(spores_pink, spores)
print('Pink spore center positions: ', pink_centers)

frame_dims = image.shape
frame_center = ((frame_dims[1]-1)/2, (frame_dims[0]-1)/2)
print(frame_center)

rs = process_centers(red_centers, frame_dims)
ps = process_centers(pink_centers, frame_dims)
bs = process_centers(blue_centers, frame_dims)

seq_str, seq_array, scores = init_seq(frame_dims, red_centers, pink_centers, blue_centers)
sorted_array ,sorted_str = sort_seq(seq_str, scores, seq_array)
print('Sequence of spores: ', sorted_str)

seg_er_type = find_type(sorted_array, sorted_str)
print("Segregation error type: ", seg_er_type)

