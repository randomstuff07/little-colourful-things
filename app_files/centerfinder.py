import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils

def red_spores(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    res = image.copy()
    lower_blue = np.array([200, 0, 0])
    upper_blue = np.array([255, 255, 200])
    mask_blue = cv2.inRange(image, lower_blue, upper_blue)
    res = cv2.bitwise_and(image, image, mask = mask_blue)
    return res

def blue_spores(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([175,100,20])
    upper2 = np.array([190,255,255])
    
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)

    full_mask = lower_mask + upper_mask

    res = cv2.bitwise_and(image, image, mask = full_mask)
    return res

def pink_spores(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    up = np.array([166, 255, 255])
    lp = np.array([150, 100, 0])
    mp = cv2.inRange(hsv, lp, up)
    res = cv2.bitwise_and(image, image, mask = mp)
    return res

def find_centers(image, spores):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	spgray = cv2.cvtColor(spores, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	plt.subplot(1, 3, 1)
	plt.imshow(thresh)
	plt.title('threshold image')
	

	kernel = np.ones((3,3),np.uint8)
	opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
	# sure background area
	sure_bg = cv2.dilate(opening,kernel,iterations=3)
	# Finding sure foreground area
	dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
	ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
	# Finding unknown region
	sure_fg = np.uint8(sure_fg)
	unknown = cv2.subtract(sure_bg,sure_fg)
	ret, markers = cv2.connectedComponents(sure_fg)
	# Add one to all labels so that sure background is not 0, but 1
	markers = markers+1
	# Now, mark the region of unknown with zero
	markers[unknown==255] = 0
	# plt.subplot(1, 3, 2)
	# plt.imshow(markers)
	# plt.title('sure fg')

	markers = cv2.watershed(spores,markers)
	spores[markers == -1] = [255,0,0]
	# plt.subplot(1, 3, 3)
	# plt.imshow(markers)
	# plt.title('watershed masks')
	# plt.show()
	
	mask_center_coords = []
	for marker in np.unique(markers):
		if marker == 0:
			continue
		# otherwise, allocate memory for the label region and draw
		# it on the mask
		mask = np.zeros(spgray.shape, dtype="uint8")
		mask[markers == marker] = 255
		# detect contours in the mask and grab the largest one
		cntrs = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cntrs = imutils.grab_contours(cntrs)
		c = max(cntrs, key=cv2.contourArea)
		# draw a circle enclosing the object
		((x, y), r) = cv2.minEnclosingCircle(c)
		cv2.circle(spores, (int(x), int(y)), int(r), (0, 255, 0), 2)
		# cv2.putText(spores, "#{}".format(marker), (int(x) - 10, int(y)),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		mask_center_coords.append((x, y))
	
	frame_dims = image.shape
	frame_center = ((frame_dims[1]-1)/2, (frame_dims[0]-1)/2)
	
	centers = []
	for center in mask_center_coords:
		if center != frame_center:
			centers.append(center)

		# print(centers)
	
	return centers


# plt.imshow(spores)
# plt.show()


