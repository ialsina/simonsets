#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 10:40:02 2020

@author: ivan
"""

import cv2
from connection import shootpic
import matplotlib.pyplot as plt
import numpy as np
from functions import *
from classification import classification


img = cv2.imread('full_image.jpeg')  # cv2 uses BGR

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert to RGB
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to HSV
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale

# Then we define the color thresholds in the HSV space

low_red = np.array([161, 80, 100])
high_red = np.array([179, 255, 255])
red_mask = cv2.inRange(img_hsv, low_red, high_red)

low_green = np.array([40, 100, 100])
high_green = np.array([90, 255, 255])
green_mask = cv2.inRange(img_hsv, low_green, high_green)

low_blue = np.array([110, 100, 50])
high_blue = np.array([130, 255, 255])
blue_mask = cv2.inRange(img_hsv, low_blue, high_blue)

# We apply a Canny edge detector

edges = cv2.Canny(img_gray, 200, 500)

# We find the contours

contours = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


cv2.drawContours(img_gray, contours[0], -1, 255, thickness=5)

for idx in range(len(contours[0])):
    print(idx)
    mask = np.zeros_like(img_gray) # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, contours[0], idx, 255, -1) # Draw filled contour in mask
    
    perc_nonzero = np.count_nonzero(mask) / (mask.shape[0]*mask.shape[1])
    
    if perc_nonzero < 0.01 : continue

    out = np.zeros_like(img) # Extract out the object and place into output image
    out[mask == 255] = img[mask == 255]

    cropped_img = np.where(mask == 255)

    # Show the output image
    col, fil, shape, num = classification(out)
    print('Number: {c}, Shape: {f}, Color: {s}, Filling: {n}'.format(c=col, f=fil, s=shape, n=num))
