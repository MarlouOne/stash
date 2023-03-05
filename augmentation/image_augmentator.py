import cv2
import numpy as np
import json
from pprint import pprint
from math import sqrt

from time import sleep
import sys
from random import choice, randint
import os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем 
import json_handler 
import matplotlib.pyplot as plt

print(f'{__name__} is here !')

class Image():
    height : int
    width  : int
    name : str
    background : cv2.Mat
    mask : cv2.Mat
    objects = []
    
    def __init__(self) -> None:
        pass
    
    def set_background(self, file_path : str) -> None:
        self.background = cv2.imread(file_path) # загружаем фото
        self.height = self.background.shape[0]
        self.width  = self.background.shape[1]
        
    def set_size(self, height = 1024, width = 1024) -> None:
        self.background = cv2.resize(self.background, (height, width)) # Меняем размер фото с параметрами в виде кортежа (ширина, высота)
    
    def set_name(self, name) -> None:
        self.name = name
        
    def add_obj(self, file_path : str, label, color : int) -> None:
        obj = Image_object()
        obj.set_label(label)
        obj.set_image(file_path, self.height, self.width, color)
        obj.set_size()
        # obj.show()
        self.objects.append(obj)
    
    def get_image(self) -> None:
        for object in self.objects:
            rows, cols = object.image.shape[:2]
            roi = self.background[:rows, :cols]

            # Создать маску
            img2gray = cv2.cvtColor(object.image, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            # Сохраните фон, кроме логотипа
            img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            dst = cv2.add(img1_bg, object.image)  # Выполнить фьюжн
            self.background[:rows, :cols] = dst  # Ставим на исходное изображение после слияния
        
        # cv2.imshow('background', self.background)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()   
            
    def show_all_masks(self):
        plt.figure(figsize=(10, 10 ))
        for i in range ( len(self.objects)):
            plt.subplot(5,5,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.objects[i].mask)
        plt.show()
    
    def show_all_image(self):
        plt.figure(figsize=(10, 10 ))
        for i in range ( len(self.objects)):
            plt.subplot(5,5,i+1)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(self.objects[i].image)
        plt.show()

    '''def get_mask(self, height = 1024, width = 1024) -> None:
        convas = np.zeros( ( height, width, len(self.objects)) , dtype='uint8') # zeros
        buffer = []
        for item in self.objects: buffer.append(item.mask)
        convas = cv2.merge(buffer) # Объединение цветовых слоёв
            
        self.mask = convas
    '''
    def get_mask(self, height = 1024, width = 1024) -> None:
        convas = np.zeros( ( height, width, 3) , dtype='uint8') # zeros
        for object in self.objects:
            rows, cols = object.mask.shape[:2]
            roi = convas[:rows, :cols]

            # Создать маску
            ''' img2gray = cv2.cvtColor(object.mask, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)'''
            ret, mask = cv2.threshold(object.mask, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)

            # Сохраните фон, кроме логотипа
            img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            dst = cv2.add(img1_bg, object.mask)  # Выполнить фьюжн
            convas[:rows, :cols] = dst  # Ставим на исходное изображение после слияния 
        self.mask = convas
        
    def drop_data(self) -> None:
        self.height     = -1 
        self.width      = -1
        self.name       = ''
        self.background = cv2.Mat
        # self.mask       = cv2.Mat
        self.objects    = []
        
    def save(self, image_path : str, mask_path : str, file_name : str, CLASSES : list) -> None:
        #save matrix/array as image file
        # class_buffer = CLASSES.copy()
        image_path = image_path + '\\' + f'image_{file_name}.png'
        image_isWritten = cv2.imwrite(image_path, self.background)
        if image_isWritten: print(f'Image {file_name} is successfully saved as file.')

        current_labels = self.get_current_labels()
        print(current_labels)

        for key in CLASSES.keys():
            if key in current_labels:
                index = current_labels.index(key)
                current_mask_path  = mask_path +  '\\' + f'mask_{file_name}_{self.objects[index].label}.png'   
                print(current_mask_path)
                # show_image( self.objects[index].mask )     
                mask_isWritten = cv2.imwrite(current_mask_path, self.objects[index].mask)
            else:
                current_mask_path  = mask_path +  '\\' + f'mask_{file_name}_{key}.png'        
                # show_image( np.zeros( ( self.height, self.width, 1) , dtype='uint8') )
                mask_isWritten = cv2.imwrite( current_mask_path, np.zeros( ( 1024, 1024, 1) , dtype='uint8') ) # zeros)

    def get_current_labels(self) -> list:
        result = []
        for item in self.objects:
            result.append(item.label)
        return result
    

class Image_object():
    label : str
    color : int
    image : cv2.Mat
    mask  : cv2.Mat
    
    def __init__(self) -> None:
        pass
    
    def set_label(self, label : str) -> None:
        self.label = label
        
    
    def set_image(self, file_path : str, height : int, width : int, color : int) -> None:
        self.color = color
        
        img1 = np.zeros( ( height, width, 3) , dtype='uint8') # zeros
        img2 = cv2.imread(file_path) # загружаем фото
        
        # print(img2.shape)
        
        
        x = randint(0, img1.shape[0]-img2.shape[0])
        y = randint(0, img1.shape[1]-img2.shape[1])

        # Разместите логотип в верхнем левом углу, чтобы нас интересовала только эта область
        rows, cols = img2.shape[:2]
        roi = img1[:rows, :cols]

        # Создать маску
        img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Сохраните фон, кроме логотипа
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        dst = cv2.add(img1_bg, img2)  # Выполнить фьюжн
        # mask = cv2.add(img1_bg, mask)  # Выполнить фьюжн
        img1[x:rows+x, y:cols+y] = dst  # Ставим на исходное изображение после слияния
        
        self.image = img1
        
        hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 0, 1])
        upper = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        '''self.mask = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        h, w = mask.shape
        r = mask.reshape( (h,w,1) )
        g = mask.reshape( (h,w,1) )
        b = mask.reshape( (h,w,1) )
        r[np.all(r != (0), axis=-1)] = (color)
        g[np.all(g != (0), axis=-1)] = (color)
        b[np.all(b != (0), axis=-1)] = (color)
        mask = cv2.merge([r,g,b]) # Объединение цветовых слоёв
        mask = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        '''
        
        h, w = mask.shape
        mask = mask.reshape( (h,w,1) )
        mask[np.all(mask != (0), axis=-1)] = (color)
        
        self.mask = mask
        
    def set_size(self, height = 1024, width = 1024) -> None:
        self.image = cv2.resize(self.image, (height, width)) # Меняем размер фото с параметрами в виде кортежа (ширина, высота)
         
        self.mask  = cv2.resize(self.mask, (height, width)) # Меняем размер фото с параметрами в виде кортежа (ширина, высота)

    def show(self) -> None:
        plt.subplot(1, 2, 1)
        plt.imshow(self.image)
        plt.subplot(1, 2, 2)
        plt.imshow(self.mask)
        plt.show()

def show_image(image : cv2.Mat) -> None:
    plt.imshow(image)
    plt.show()

def get_random_item(directory):
    items = os.listdir( directory ) 
    return choice(items)

def get_palette(CLASS : list):
    colors = [i for i in range(50, 255, 205//len(CLASS))]
    return dict(zip(CLASS, colors))

def main(image_count : int , directory : str, min_obj_count = 1) -> None:
    
    CLASS = os.listdir( directory + '\image' ) 
    
    CLASS = get_palette(CLASS)
    print( CLASS )
    
    
    image_path = r'augmentation\results\argus\image'
    mask_path  = r'augmentation\results\argus\mask'
    
    img = Image()  
    
    for i in range( image_count ):
        class_buffer = CLASS.copy()
        
        img.set_name('image')
        img.set_background( directory + '\\back\\' + get_random_item( directory + '\\back') )
        img.set_size()
        
        
        print( len(img.objects) )
        
        
        # print(len(class_buffer.keys()), len(CLASS.keys()))
        for item in range( randint( min_obj_count, len(class_buffer.keys())) ):
            rand_CLASS = choice(list(class_buffer.keys()))
            rand_ITEM  = get_random_item(directory + '\\image\\' + rand_CLASS )
            
            # print(rand_CLASS, rand_ITEM)
            
            img.add_obj(directory + '\\image\\' + rand_CLASS + '\\' + rand_ITEM, rand_CLASS, CLASS[rand_CLASS])
            
            
            
            del class_buffer[rand_CLASS] # CLASS.remove(rand_CLASS) 
            
        img.get_image()
        # img.show_all_image()
        # img.show_all_masks()
        # img.get_mask()
        img.save(image_path, mask_path, str(i), CLASS)
        
        # show_image(img.background)
        # show_image(img.mask)
        
        img.drop_data()
        
if __name__ == '__main__': 
    directory = r'augmentation\samples\argus'
    image_count = 1
    # directory = r'Machine_vision\src\test_json'
    main(image_count,directory)

