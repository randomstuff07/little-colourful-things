import torch
import subprocess
import matplotlib.pyplot as plt
import numpy as np


from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
SAM_CHKPT_PATH = '/Users/aaditmahajan/Documents/Summer_Internship/sam_vit_h_4b8939.pth'
model_type = 'vit_h'
sam = sam_model_registry[model_type](checkpoint=SAM_CHKPT_PATH)
sam.to(device=device)

init_mask_gen = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side = 12,
    pred_iou_thresh = 0.9,
    stability_score_thresh=0.92,
    crop_n_layers=1,
    min_mask_region_area=1000,
    crop_n_points_downscale_factor=2
)
ind_cell_mask_gen = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side = 7,
    pred_iou_thresh = 0.8,
    stability_score_thresh=0.8,
    crop_n_layers=1,
    min_mask_region_area=4000,
    crop_n_points_downscale_factor=2
)

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x:x['area']), reverse=True)
    ax = plt.gca()
    # ax.set_autoscale_on(False)
    polygons = []
    color = []
    for ann in sorted_anns:
        m = ann['segmentation']
        img = np.ones((m.shape[0], m.shape[1], 3))
        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            img[:,:,i] = color_mask[i]
        ax.imshow(np.dstack((img, m*0.35)))

def generate_mask(image, generator):
    masks = generator.generate(np.asarray(image, dtype='uint8'))
    return masks

def show_mask(image, masks):
    print('No of detected cells = ', len(masks))
    plt.figure(figsize=(8, 5))
    plt.subplot(121)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(image)
    show_anns(masks)
    plt.axis('off')
    plt.show()

def separate_clusters(masks, raw):
    individual_cells = []
    clusters = []
    cropped_rois = []

    for i in range(len(masks)):
        x=int(masks[i]['bbox'][0])
        y=int(masks[i]['bbox'][1])
        a=int(masks[i]['bbox'][2])
        b=int(masks[i]['bbox'][3])
        cropped_im = raw[y:y+b, x:x+a, :]
        cropped_rois.append(cropped_im)
        cropped_mask = masks[i]['segmentation'][y:y+b, x:x+a]
        plt.imshow(cropped_im)
        plt.show()
        area = masks[i]['area']
        if area in range(2000, 3000):
            individual_cells.append(cropped_im)
        elif area > 3000:
            clusters.append(cropped_im)
        else:
            continue
    return individual_cells, clusters

def process_cluster(clusters):
    individual_cells = []
    for cluster in clusters:
        mask_cluster = generate_mask(np.asarray(cluster, dtype='uint8'), ind_cell_mask_gen)
        show_mask(cluster, mask_cluster)
        for j in range(len(mask_cluster)):
            x=int(mask_cluster[j]['bbox'][0])
            y=int(mask_cluster[j]['bbox'][1])
            a=int(mask_cluster[j]['bbox'][2])
            b=int(mask_cluster[j]['bbox'][3])
            cropped_im = cluster[y:y+b, x:x+a, :]
            area = mask_cluster[j]['area']

            if area in range(1500, 3000):
                individual_cells.append(cropped_im)
                plt.imshow(cropped_im)
                plt.show()
                print('added to individual cells array....')

    return individual_cells

