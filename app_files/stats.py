import cv2
from centerfinder import *
from seq_finder import *
import numpy as np

def stats(cell_array):

    error_count = np.zeros(7)
    '''
    this error count array is updated according to the following indexing:
    1. normal 
    2. cco
    3. mi ndj
    4. mi rs
    5. mi pssc 
    6. mii pssc
    7. others
    '''

    for cell in cell_array:

        image = cell
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        spores_red = red_spores(image)
        spores_blue = blue_spores(image)
        spores_pink = pink_spores(image)

        # plt.subplot(1, 3, 1)
        # plt.imshow(spores_red)
        # plt.title('Red Spores')
        # plt.subplot(1, 3, 2)
        # plt.imshow(spores_blue)
        # plt.title('Blue Spores')
        # plt.subplot(1, 3, 3)
        # plt.imshow(spores_pink)
        # plt.title('Pink Spores')
        # plt.show()

        spores = spores_red+spores_pink+spores_blue
        # spgray = cv2.cvtColor(spores, cv2.COLOR_BGR2GRAY)

        # print('RED MASKS: ')
        red_centers = find_centers(spores_red, spores)
        # print('Red spore center positions: ', red_centers)
        # print('----------------------------------------------------------------')
        # print('BLUE MASKS: ')
        blue_centers = find_centers(spores_blue, spores)
        # print('Blue spore center positions: ', blue_centers)
        # print('----------------------------------------------------------------')
        # print('PINK_MASKS: ')
        pink_centers = find_centers(spores_pink, spores)
        # print('Pink spore center positions: ', pink_centers)

        frame_dims = image.shape
        # frame_center = ((frame_dims[1]-1)/2, (frame_dims[0]-1)/2)
        # print(frame_center)

        seq_str, seq_array, scores = init_seq(frame_dims, red_centers, pink_centers, blue_centers)

        sorted_array ,sorted_str = sort_seq(scores, seq_array, img_dims=frame_dims)
        # print('Sequence of spores: ', sorted_str)

        seg_er_type = find_type(sorted_array, sorted_str)
        # print("Segregation error type: ", seg_er_type)

        error_key = {
            'normal'    :0,
            'cco'       :1,
            'mi_ndj'    :2,
            'mi_rs'     :3,
            'mi_pssc'   :4,
            'mii_pssc'  :5,
            'others'    :6
        }

        index = error_key[seg_er_type]
        error_count[index] += 1

    categories = ['Normal', 'CCO', 'MI NDJ', 'MI RS', 'MI PSSC', 'MII PSSC', 'Others']
    return categories, error_count 






