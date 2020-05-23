#!/usr/bin/env python
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

img_loc = r'/home/dnl/Downloads/circles.jpg'
ogi = cv.imread(cv.samples.findFile(img_loc))
img = cv.imread(img_loc, 0)
if img is None:
    print('Could not load img :(')

img = cv.medianBlur(img, 5)
cimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)


circles = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=65, maxRadius=80)
circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    print(f'-> Radius = {i[2]}')
    cv.circle(cimg, (i[0], i[1]), i[2], (0,255,0),2)
    cv.circle(cimg, (i[0], i[1]), 2, (0,0,255),3)
cv.imshow('Road', ogi)
cv.imshow('Road', cimg)
k = cv.waitKey(0)

if k == ord('s'):
    cv.imwrite('damn.jpg', img)
