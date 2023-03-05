import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_image(image : cv2.Mat) -> None:
    plt.imshow(image)
    plt.show()


def resize_image(image : cv2.Mat ,ratio : float) -> cv2.Mat:
    return cv2.resize(image, ( int(image.shape[1]*ratio), int(image.shape[0]*ratio) ) )

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
    mask = cv2.inRange(hsv_img, color_low,  color_high) # наложение цветовой маски на HSV-изображение
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = contours[1]
    if contours:
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        cv2.drawContours(image, contours, -1, (255, 0 , 255), 3)
        show_image(image)
    return image

def show_contours(source_image : cv2.Mat, image : cv2.Mat, limit_area = 10) -> cv2.Mat:

    canny = cv2.Canny(image, 100, 255)
    show_image(canny)
    
    contours, h = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Находим контуры изображения
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > limit_area:
            cv2.drawContours(source_image, contour, -1, (200, 200, 0), 3)
            p = cv2.arcLength( contour, True)
            num = cv2.approxPolyDP(contour, 0.03*p, True)
            x,y,w,h = cv2.boundingRect(num)
            cv2.rectangle( source_image, (x, y, x + w, y + h), (0,0,256), 4)
            
    return source_image


photo_path = r'Machine_vision\Datasets\argus\base\  (6).jpg'
source_image = cv2.imread(photo_path) # загружаем фото

source_image = resize_image(source_image, 0.2)

red_box = find_red_box(source_image)
yellow_ball = find_yellow_ball(source_image)

# show_image(red_box)
# show_image(yellow_ball)

red_box     = show_contours( source_image, red_box     )
yellow_ball = show_contours( source_image, yellow_ball )



# counterts = cv2.findContours(red_box, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# show_image(red_box)
# show_image(yellow_ball)



# show_image(image_colored)

# adjustment(image_colored)
