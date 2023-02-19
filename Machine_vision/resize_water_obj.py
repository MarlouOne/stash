import cv2
import numpy as np
import psutil
import os

directory_img  = 'Machine_vision\Datasets\Satellite_Images_of_Water_Bodies\Water Bodies Dataset\Images'
directory_mask = 'Machine_vision\Datasets\Satellite_Images_of_Water_Bodies\Water Bodies Dataset\Masks'

print( len(os.listdir(directory_img)), len(os.listdir(directory_mask))  )
 

# for file in os.listdir(directory): 

    # filename = os.path.join(directory, file)
    # if os.path.isfile(filename):
    #     # print(filename)
    #     file_counter += 1


    