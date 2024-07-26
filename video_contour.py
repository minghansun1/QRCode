import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    contours,_ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)

    i = 0
    for contour in contours:
        if i == 0:
            i = 1
            continue
        approx = cv2.approxPolyDP(contour, 0.1*cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 2)

    cv2.imshow("image", img)
    cv2.waitKey(1)

cap.release()