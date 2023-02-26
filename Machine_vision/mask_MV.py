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

print(f'{__name__} is here !')

class Img():
    height : int
    width  : int
    name : str
    masks = []
    
    def __init__(self, heigth : int, width : int, name : str) -> None:
        self.height = heigth
        self.width = width
        self.name = name
    
    def __init__(self, content : dict) -> None:
        # print(content.keys())
        
        self.height = content['imageHeight']
        self.width  = content['imageWidth']
        self.name   = 'mask_' + content['imagePath']
        for item in content['shapes']:
            # print(item.keys())
            self.set_masks(item)
        
    def shape(self) -> tuple:
        return (self.height, self.width)
    
    def set_heigth(self, heigth : int) -> None:
        self.height = heigth
    
    def set_width(self, width : int) -> None:
        self.width = width
        
    def set_name(self, name : str) -> None:
        self.name = name
    
    def set_masks(self, mask : dict) -> None: #content : dict
        # for mask in content['shapes']:
        self.masks.append( Mask(
                                    self.height,
                                    self.width,
                                    self.name,
                                    mask["label"],
                                    mask["shape_type"],
                                    mask["points"]
                                    # np.array( mask["points"], np.int32 )
                               )
                        )
    
    def show(self) -> None:
        print(self.shape(), self.name, sep=' | ')
        for item in self.masks:
            pprint(item)
    
    def from_json(self, content : dict):
        for item in content['shapes']:
            self.height = item['imageHeight']
            self.width  = item['imageWidth']
            self.name   = 'mask_' + item['imagePath']
            self.set_masks(item)
    
        
class Mask(Img):
    label : str
    shape_type : str
    points : list
    
    def __init__(self, heigth : int, width : int, name : str, label : str, shape_type : str, points : list) -> None:
        self.height = heigth
        self.width = width
        self.name = name
        
        self.label = label
        self.shape_type = shape_type
        self.points = list_float2int( points )   
    
    def get_mask(self, height = 1000, width = 1000, color = (255, 255, 0)) -> cv2.Mat:
        
        # create and reshape array
        size = (self.shape()[0], self.shape()[1], 3)
        image = np.zeros(size, dtype='uint8') # zeros
        pts = [np.int32(self.points)] 

        if self.shape_type == 'polygon':
            image = cv2.polylines(img = image, pts = pts, isClosed = True,  color = color, thickness = 8, lineType=cv2.LINE_AA ,)
            image = cv2.fillPoly(image, pts, color = color)
            
        elif self.shape_type == 'circle':
            c_radius = sqrt( (self.points[1][1] - self.points[0][1])**2 + (self.points[1][0] - self.points[0][0])**2 )
            cv2.circle(image, center = (self.points[0]), radius = int(c_radius), color = color, thickness = -1)
        
        # Displaying the image
        while(1):
            image = cv2.resize(image, (height, width)) # Меняем размер фото с параметрами в виде кортежа (ширина, высота)
            cv2.imshow(f'{self.label}', image)
            if cv2.waitKey(20) & 0xFF == 27: # Escape
                break
        cv2.destroyAllWindows()
        
        return image
        
def list_float2int(content : list) -> list:
    result = []
    for lists in content:
        buffer = []
        for item in lists:
            buffer.append( int(item) )
        result.append( buffer )
    return result

def tuple_float2int(content : tuple) -> tuple:
    result = []
    for item in content:
        result.append( int(item) )
    return result

def main(directory : str):
    
    buffer = []
    
    for file in os.listdir(directory): 
    
        
        filename = os.path.join(directory, file) # checking if it is a file
        
        if not os.path.isfile(filename):
            continue
             
        # print(filename)
        obj = json_handler.read_json(filename)
        obj = Img(obj)
        buffer.append(obj)
    
    labels = []

    for image in buffer:
        for masks in image.masks:
            if masks.label not in labels : labels.append( masks.label )
    
    print( labels , '|', len( labels ) )
    # Todo : Надо собрать список всей объектов и раскрасить их по определённым цветам, а потом собрать их в одно фото
        # obj.show()
        
        # for item in obj.masks:
        #     item.show_mask()

        

if __name__ == '__main__': 
    directory = r'Machine_vision\Datasets\argus\json_mask'
    # directory = r'Machine_vision\src\test_json'
    main(directory)

