import cv2
import numpy as np

img = cv2.imread('ekg-proba.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

cv2.imshow("binary", binary_image)


# Usuń szum za pomocą medianowego filtra
filtered_image = cv2.medianBlur(binary_image, 3)


kernel_opening = np.ones((5, 5), np.uint8)
opened_edges = cv2.morphologyEx(filtered_image, cv2.MORPH_OPEN, kernel_opening)


cv2.imshow('open', opened_edges)

ret,thresh = cv2.threshold(opened_edges,180,255,0)
cv2.imshow('thres', thresh)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
print("Number of contours detected:", len(contours))

# Draw contours on the original image
contour_image = img.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)  # -1: draw all contours, (0, 255, 0): color, 2: thickness

# Display the image with contours
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()