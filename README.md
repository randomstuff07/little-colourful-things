# little-colourful-things v1.0

Description of functions defined in the py files in this folder. 

_centerfinder.py_ file methods:

1. red_spores(image)
   finds the red spores, returns an image with red spores isolated from the raw image
   returns isolated red spores image

2. blue_spores(image)
   finds the blue spores, returns an image with blue spores isolated from the raw image
   returns isolated blue spores image

3. pink_spores(image)
   finds the pink spores, returns an image with pink spores isolated from the raw image
   returns pink spores image

4. find_centers(image, spores):
   finds the centres of the spore image passed to it
   uses watershed segmentation
   returns an array of coordinates (x, y) of the centres of the spore image passed

_seqfinder.py_ file methods 

1. process_centers(centers, img_dims)
   uses the centre coordinates and image dimensions to assign position-wise scores to each centre
   returns scores

2. init_seq(image, red_centers, pink_centers, blue_centers)
   finds the unsorted sequence based on how many spores of each colour are present. 
   passes an array of alphabets based on which colour is present and a string of the colour-coded sequence

3. sort/_seq(seq_string, scores, sequence)
   finds the correct order of the spores in the cell using the scores assigned to each spore centre
   returns a sorted string sequence and the corresponding sorted string sequence

4. find_type(sequence, seq_string)
   finds the type of error based on a key (credits: MN Lab) for the error types and the sequences of the colours of the spores in each error type. 
   returns a string containing the type of error

_pizzacutter.py_ file details:

**DO NOT CHANGE THESE**:

init_mask_gen constants:

    model=sam,
    points_per_side = 12,
    pred_iou_thresh = 0.9,
    stability_score_thresh=0.92,
    crop_n_layers=1,
    min_mask_region_area=1000,
    crop_n_points_downscale_factor=2

this is the configuration for the constants for generating the masks initially for the whole frame. 

ind_cell_mask_gen constants:

    model=sam,
    points_per_side = 7,
    pred_iou_thresh = 0.8,
    stability_score_thresh=0.8,
    crop_n_layers=1,
    min_mask_region_area=4000,
    crop_n_points_downscale_factor=2
   
This is the configuration for the constants for generating the masks from the clusters cut out by the initial mask generator and identifies individual cells from the clusters. 

_pizzacutter.py_ file methods:

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

