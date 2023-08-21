import cv2
import imutils
import os
import matplotlib.pyplot as plt
import numpy as np
import torch

def load_images(IMG_FILE_PATH):
    images = []
    for filename in os.listdir(IMG_FILE_PATH):
        img = cv2.imread(os.path.join(IMG_FILE_PATH,filename))
        if img is not None:
            images.append(img)
    return images

def preprocess_image_low_cont(image):
    torch.set_default_dtype(torch.float32)
    plt.imshow(image)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale,150,25)
    # edges = cv2.erode(edges, kernel = cv2.getStructuringElement(cv2.MORPH_ERODE, (3, 3)), iterations=1)

    plt.subplot(121),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    edges_3d_array = np.zeros((1080, 1080, 3))
    for i in range(3):
        edges_3d_array[:, :, i] = edges

    edges_3d_array = cv2.GaussianBlur(edges_3d_array, (3, 3), 0)
    plt.imshow(edges_3d_array)

    plt.show()
    return edges_3d_array

def preprocess_image_high_cont(image):

    plt.imshow(image)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # first isolate blue spores
    result = image.copy()
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])
    
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)

    full_mask = lower_mask + upper_mask

    result_blue = cv2.bitwise_and(result, result, mask = lower_mask)
    
    # next isolate red spores 
    lower_blue = np.array([100, 100, 20])
    upper_blue = np.array([140, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    result_red = cv2.bitwise_and(image, image, mask = mask_blue)
    spores = result_red + result_blue

    # next isolate pink spores 
    lower_pink = np.array([100, 100, 20])
    upper_pink = np.array([140, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    result_red = cv2.bitwise_and(image, image, mask = mask_blue)

    # now do thresholding on total spore image
    spores_grayscale = cv2.cvtColor(cv2.cvtColor(spores, cv2.COLOR_BGR2HSV), cv2.COLOR_BGR2GRAY)

    th = cv2.adaptiveThreshold(spores_grayscale,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

    erosion = np.array(
        [   
            [1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1],
            [1, 1, 1 ,1, 1],
            [1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1]
        ]
      )

    for erode_iter in range(0, 3):
        thick_bounds = cv2.erode(cv2.dilate(th, kernel=erosion, iterations= 1), kernel=erosion, iterations= 1)

    # th = cv2.dilate(thick_bounds, kernel = erosion, iterations = 1)

    plt.subplot(121),plt.imshow(image,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(th,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    edges_3d_array = np.zeros((1080, 1080, 3))
    for i in range(3):
        edges_3d_array[:, :, i] = thick_bounds

    # edges_3d_array = cv2.GaussianBlur(edges_3d_array, (3, 3), 0)
    plt.imshow(edges_3d_array)

    plt.show()
    return edges_3d_array






