import cv2
import numpy as np

def rotate(img, angle):
    ##Функция вращения картинки на определённый угол
    height, width = img.shape[:2]
    point = (width//2, height//2)
    
    mat = cv2.getRotationMatrix2D(point, angle, 1)
    return cv2.warpAffine(img, mat, (width, height))


def nothing(x):
    pass

img = cv2.imread(r'Machine_vision\src\boxs.jpg') # загружаем фото
cv2.imshow('Photo', img) # Показываем фото

cv2.namedWindow('track')
cv2.createTrackbar('T1','track',0,255,nothing)
cv2.createTrackbar('T2','track',0,255,nothing)

kernel = np.ones((5,5), np.uint8) # Создаём матрицу границ

while True:
    frame = cv2.bilateralFilter(img, 9, 75, 75)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Приводим картинку к Ч/Б варианту

    thresh1 = cv2.getTrackbarPos('T1', 'track')
    thresh2 = cv2.getTrackbarPos('T2', 'track')

    canny = cv2.Canny(gray, thresh1, thresh2)
    dil = cv2.dilate(canny, kernel, iterations=1)
    
    contours, hir = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Находим контуры изображения


    cv2.imshow('Frame', frame)
    cv2.imshow('Gray', gray)
    cv2.imshow('Dil', dil)
    cv2.imshow('Canny', canny)
    
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27: break
    
cv2.destroyAllWindows()