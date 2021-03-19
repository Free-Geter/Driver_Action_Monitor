import cv2

image = "image1.jfif"
image = cv2.imread(image)

cv2.namedWindow("resized",0);
cv2.resizeWindow("resized", 640, 480);
cv2.imshow("resized",image)
cv2.waitKey(0)
