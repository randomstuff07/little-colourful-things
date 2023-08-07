import cv2
import imutils
import os
import matplotlib.pyplot as plt
import numpy as np

def load_images(IMG_FILE_PATH):
    images = []
    for filename in os.listdir(IMG_FILE_PATH):
        img = cv2.imread(os.path.join(IMG_FILE_PATH,filename))
        if img is not None:
            images.append(img)
    return images

def preprocess_image(image):
  
    plt.imshow(image)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(grayscale,500,50)
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







