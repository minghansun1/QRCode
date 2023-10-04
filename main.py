import cv2
import numpy as np
from pyzbar.pyzbar import decode

img = cv2.imread("1-cropped.png")

cv2.imshow("image", img)
cv2.waitKey(5000)