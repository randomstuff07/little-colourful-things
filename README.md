**Little Colourful Things** v1.0
---
## Overview:
Little Colourful Tings is a Python application designed for the efficient analysis of fluorescent images of yeast cells. This application processes image data and provides comprehensive statistics to aid in a foresight into experiments. 

### Key Features:

Image Import: Easily import fluorescent yeast cell images in various formats, including TIFF, JPEG, and PNG.    
Automated Cell Detection: The tool automatically detects and isolates individual yeast cells within the images. It uses the Segment Anything Model to achieve this.     
Statistical Analysis: Generate essential statistical metrics for each frame, showing the segregation assay error metrics for a batch of images.     
User-Friendly Interface: The tool features an intuitive graphical user interface (GUI) that makes it accessible to both beginners and experienced users.    
### Installing/Running instructions:

1. Clone the repository 
2. Add the images to be processed to a file named dataset (kindly do not make subfolders in this folder)
3. Download the checkpoints file and place it in the app_files folder of the repo. (Cannot place this file in the repository as it is too large)
4. Open command prompt/terminal
5. Enter 'cd your_file_path_to_the_repository and hit enter
6. Run pip install -r config.txt
7. Run 'python exec.py'

### Dependencies:

Python 3.x
SAM ViT-B checkpoints (file link: https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth)
OpenCV for image processing
NumPy for numerical operations
Matplotlib for data visualization
Segment Anything model for segmentation
Flet for GUI

### Installation:

Clone or download the repository.
Install the required dependencies using pip install -r config.txt.

### Usage:    
Run the program by using the command 'python exec.py'
Follow the on-screen instructions to load and analyze your fluorescent yeast cell images.

### License:
This project is licensed under the Apache License Version 2.0 License. Feel free to use, modify, and distribute it in accordance with the terms of the license.

### Authors:

Aadit Mahajan 

### Acknowledgements:
A big thanks to Dr. Mridula Nambiar and MN Lab, IISER Pune for giving me this opportunity. I appreciate all the support that I recieved while completing this project and I hope that this project will aid research in the lab. 

I also express my gratitude to my family and to all my friends for giving inputs to tackle the hurdles during the course of this project. Thanks a lot.

---
## Description of functions defined in the py files in this folder. 
---
_centerfinder.py_ file methods:

1. red_spores(image)   
   finds the red spores, returns an image with red spores isolated from the raw image


2. blue_spores(image)  
   finds the blue spores, returns an image with blue spores isolated from the raw image


3. pink_spores(image)  
   finds the pink spores, returns an image with pink spores isolated from the raw image

4. find_centers(image, spores):  
   finds the centres of the spore image passed to it
   uses watershed segmentation
   returns an array of coordinates (x, y) of the centres of the spore image passed

*seq_finder.py* file methods 

1. process_centers(centers, img_dims)  
   uses the centre coordinates and image dimensions to assign position-wise scores to each centre
   returns scores

2. init_seq(image, red_centers, pink_centers, blue_centers)   
   finds the unsorted sequence based on how many spores of each colour are present. 
   passes an array of alphabets based on which colour is present and a string of the colour-coded sequence

3. sort_seq(seq_string, scores, sequence)    
   finds the correct order of the spores in the cell using the scores assigned to each spore centre
   returns a sorted string sequence and the corresponding sorted string sequence

4. find_type(sequence, seq_string)   
   finds the type of error based on a key (credits: MN Lab) for the error types and the sequences of the colours of the spores in each error type. 
   returns a string containing the type of error   


*pizzacutter.py* file methods:

1. show_anns(anns)    
   Shows the annotations on an image (sub_function of show masks function)

2. generate_mask(image, generator)    
   generates masks using the Segment-Anything model and choosing one of the two configurations of the constants. 
   returns masks

3. show_masks(image, masks)     
   shows masks in good_looking format

4. separate_clusters(masks, raw)     
   separates clusters and/or individual cells from the raw image and puts into different arrays of images using init_mask_gen SAM constants and the generate_mask function.
   returns an array of individual cells and clusters. 

5. process_cluster(clusters)   
   separates individual cells from the cluster array passed from the function separate_clusters using the ind_cell_mask_gen SAM constants and the generate mask function
   returns an array of individual cells which is concatenated with the previous array of individual cells

*preprocess.py* file methods:

1. load_images(IMG_FILE_PATH)     
   takes the file path of the folder with all the raw images and returns an array of images for further processing. 

2. preprocess_image_low_cont(image)   
   this is image preprocessing for low contrast images (see section below to decide which config to use based on image).
   It implements Canny edge detection and gaussian blurring to return a 3d array which can be processed easier for processing as it has more defined edges around cells. 

3. preprocess_image_high_cont(image)   
   this is image preprocessing for high contrast images. 
   It implements color masking to isolate the differently colored spores from the background completely and then finding edges on the image formed by only spores. This is a much more effective method than using the same strategy as low contrast preprocessing, due to the different characteristics of the image. 

*stats.py* file methods: 

1. stats(cell_array)    
   counts the no. of segregation errors which are captured in the output ROIs of segment anything model. 
   This uses the _findcenters_ method from centerfinder.py 

*exec.py* methods:
1.  get_main_window(page: ft.Page)    
   This is the function for the startup page of the application. It takes in the file path for the raw images and passes it on to the methods which process the images further.
   This is also written using flet. 

   Important dependent functions in the get_main_window function:    
   a. def disp_stats(cats, err_cnt)      
   This is the function which displays the stats, and takes the error count and categories as input from the global variables *cats* and *err_cnt*. This is coded using flet wrapper for Flutter in python.     
   b. def chkdir(e):      
   checks if the directory passed has valid files. Then changes state of main window.         
   c. def write_config_settings(e):       
   writes the file path and the contrast settings to be used to the 'config.json' file. (default contrast setting is 'low contrast')     
   d. def open_readme(e):      
   opens this README.md file in a text editor.               
   
2. classifier():
   Takes all the inputs from the user and executes the workflow for the classification of the cells in to their respective types.

SAM Mask Generator config:
---
Following are the parameters for the segment anything automatic mask generator.

init_mask_gen = SamAutomaticMaskGenerator(    
    model=sam,     
    points_per_side = 8,      
    pred_iou_thresh = 0.8,     
    stability_score_thresh=0.8,     
    crop_n_layers=0,      
    min_mask_region_area=1800,       
    crop_n_points_downscale_factor=2       
)

This is the configuration for the constants for generating the masks initially for the whole frame. 

ind_cell_mask_gen = SamAutomaticMaskGenerator(     
    model=sam,     
    points_per_side = 8,    
    pred_iou_thresh = 0.88,    
    stability_score_thresh=0.88,    
    crop_n_layers=0,     
    min_mask_region_area=1800,     
    crop_n_points_downscale_factor=2     
)

This is the configuration for the constants for generating the masks from the clusters cut out by the initial mask generator and identifies individual cells from the clusters. 

Choosing between configurations:
---
The choice between high contrast and low contrast images has to be made wisely due to the differences in background processes implemented to improve the prediction efficiency in each setting. 

High contrast images can be considered those with low background light and fluorescent light is bright.   
Low contrast images can be considered those with a lot of background noise/bright background light and fluorescent light from spores being relatively harder to distinguish from background.    

# References

1. Kirillov, Alexander & Mintun, Eric & Ravi, Nikhila & Mao, Hanzi & Rolland, Chloe & Gustafson, Laura & Xiao, Tete & Whitehead, Spencer & Berg, Alexander & Lo, Wan-Yen & Dollár, Piotr & Girshick, Ross. (2023). Segment Anything. 
2. Bradski, G. & Kaehler, A., 2008. Learning OpenCV: Computer vision with the OpenCV library, "O&#x27;Reilly Media, Inc."

## Link to downloading the checkpoint file for the Segment Anything model    
Download here: https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth     
Save the file in app_files of the main repository.    
***(Source: Segment Anything GitHub (https://github.com/facebookresearch/segment-anything))***

