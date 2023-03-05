import cv2
import numpy as np
import matplotlib.pyplot as plt

def rotate(img, angle):
    ##Функция вращения картинки на определённый угол
    height, width = img.shape[:2]
    point = (width//2, height//2)
    
    mat = cv2.getRotationMatrix2D(point, angle, 1)
    return cv2.warpAffine(img, mat, (width, height))

def show_list_content(content : list):
    plt.figure(figsize=(10, 10 ))
    for i in range ( len(content)):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(content[i])
    plt.show()

def show_image(image : cv2.Mat) -> None:
    plt.imshow(image)
    plt.show()

def nothing(x):
    pass

def resize_image(image : cv2.Mat ,ratio : float) -> cv2.Mat:
    return cv2.resize(image, ( int(image.shape[1]*ratio), int(image.shape[0]*ratio) ) )

def adjustment(image : cv2.Mat) -> None:
    cv2.namedWindow('track')
    cv2.createTrackbar('T1','track',0,255,nothing)
    cv2.createTrackbar('T2','track',0,255,nothing)

    kernel = np.ones((5,5), np.uint8) # Создаём матрицу границ

    while True:
        frame = cv2.bilateralFilter(image, 9, 75, 75)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Приводим картинку к Ч/Б варианту

        thresh1 = cv2.getTrackbarPos('T1', 'track') # 30
        thresh2 = cv2.getTrackbarPos('T2', 'track') # 0

        canny = cv2.Canny(gray, thresh1, thresh2)
        dil = cv2.dilate(canny, kernel, iterations=1)
        
        contours, h = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS) # Находим контуры изображения CHAIN_APPROX_TC89_KCOS "55"

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1500:
                cv2.drawContours(frame, contour, -1, (200, 200, 0), 3)
                p = cv2.arcLength( contour, True)
                num = cv2.approxPolyDP(contour, 0.005*p, True)
                x,y,w,h = cv2.boundingRect(num)
                cv2.rectangle( frame, (x, y, x + w, y + h), (0,0,256), 4)

        cv2.imshow('Frame', frame)
        cv2.imshow('Gray', gray)
        cv2.imshow('Dil', dil)
        cv2.imshow('Canny', canny)
        
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27: break
        
    cv2.destroyAllWindows()

def up_sharp(image : cv2.Mat) -> cv2.Mat:
    kernel = np.array([[-1, -1, -1],                
                       [-1, 9, -1],        
                       [-1, -1, -1]])
    
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened

def to3Channals(image : cv2.Mat) -> cv2.Mat:
    if len(image.shape) == 3:
        return image
    h, w = image.shape
    r = image.reshape( (h,w,1) )
    g = image.reshape( (h,w,1) )
    b = image.reshape( (h,w,1) )
    return cv2.merge([r,g,b]) # Объединение цветовых слоёв
        
def blur_conturs(image : cv2.Mat) -> cv2.Mat:
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    low_gauss = cv2.GaussianBlur(gray_img, (55, 55), 1)
    high_gauss = cv2.GaussianBlur(gray_img, (111, 111), 111)
    image = low_gauss - high_gauss
    # Вычисление DoG    dog = low_gauss - high_gauss
    return image

def scale(image : cv2.Mat, lower = 200, higher = 255) -> cv2.Mat:
    buf_image = cv2.medianBlur(image, 1) 
    image_gray = cv2.cvtColor(buf_image, cv2.COLOR_BGR2GRAY)
    mask = cv2.Canny(image_gray, lower, higher)
    mask = to3Channals(mask)
    return cv2.addWeighted(buf_image,1,mask,0.4,0)

def find_yellow_ball(image : cv2.Mat) -> cv2.Mat:
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # конвертируем исходное изображение в HSV,
    color_low = (25,100,175) # нижняя граница — это темный ненасыщенный цвет
    color_high = (35,255,255) # верхняя граница — это яркий насыщенный цвет
    only_object = cv2.inRange(hsv_img, color_low,  color_high) # наложение цветовой маски на HSV-изображение
    return only_object
    
def find_red_box(image : cv2.Mat) -> cv2.Mat:
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # конвертируем исходное изображение в HSV,
    color_low = (0,153,153) # нижняя граница — это темный ненасыщенный цвет
    color_high = (0,255,255) # верхняя граница — это яркий насыщенный цвет
    only_object = cv2.inRange(hsv_img, color_low,  color_high) # наложение цветовой маски на HSV-изображение
    return only_object


buffer = []

photo_path = r'Machine_vision\Datasets\argus\base\  (2).jpg'
image_colored = cv2.imread(photo_path) # загружаем фото

image_colored = resize_image(image_colored, 0.2)

red_box = find_red_box(image_colored)
yellow_ball = find_yellow_ball(image_colored)

show_image(red_box)
show_image(yellow_ball)

for i in range(70):
    image_colored = scale(image_colored)




# show_image(image_colored)

# adjustment(image_colored)
