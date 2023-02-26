import cv2
import numpy as np
import json
from pprint import pprint
from math import sqrt

from time import sleep
import sys
import os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем 
import json_handler 


import cv2
import matplotlib.pyplot as plt
import numpy as np

def show_colors(lvl_color : tuple, ) -> None :
    low_img = np.zeros((300, 300, 3), np.uint8)
    low_img[:] = lvl_color[0]
    high_img = np.zeros((300, 300, 3), np.uint8)
    high_img[:] = lvl_color[1]
    
    plt.subplot(1, 2, 1)
    plt.imshow(low_img)
    plt.subplot(1, 2, 2)
    plt.imshow(high_img)
    plt.show()

def by_color(image : cv2.Mat, lvl_color_hsv : tuple, lvl_white : tuple) -> cv2.Mat :
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    # Цветовые границы региона
    low_color_hsv, high_color_hsv = lvl_color_hsv
    # Границы для белых оттенков
    low_white, high_white = lvl_white
    
    # Получение двоичной финальной маски
    mask_white = cv2.inRange(hsv_image, low_white, high_white)
    mask = cv2.inRange(hsv_image, low_color_hsv, high_color_hsv)
    final_mask = mask + mask_white
    
    # Применение маски
    result = cv2.imread('result.jpg')
    result_masked = cv2.bitwise_and(image, image, result, final_mask)
    
   
    # # Сглаживание
    # blur = cv2.GaussianBlur(result, (9, 9), 0)
    
    # Поиск краев, основанный на выбранном цветовом регионе
    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = cv2.drawContours(result_masked, contours, -1, (255, 255, 0), 3, cv2.LINE_AA, hierarchy, 1)
     # Маска и исходное изображение с маской сверху
    plt.subplot(1, 3, 1)
    plt.imshow(final_mask, "gray")
    plt.subplot(1, 3, 2)
    plt.imshow(result_masked)
    plt.subplot(1, 3, 3)
    plt.imshow(result)
    plt.show()

image = cv2.imread('Machine_vision\src\  (3).jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Повышение резкости
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
image = cv2.filter2D(image, -1, kernel)
# plt.imshow(image)
# plt.show()



# show_colors( ( (1, 190, 200), (18, 255, 255) ) )
# by_color(image, ( (1, 190, 200), (18, 255, 255) ), ( (0, 0, 200), (145, 60, 255) ) )
# show_colors( ( (216, 92, 156), (246, 92, 156) ) )
by_color(image, ( (69, 67, 55), (70, 64, 50)  ), ( (0, 0, 200), (145, 60, 255) ) )




