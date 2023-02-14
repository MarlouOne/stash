import cv2
import numpy as np

#Чтение фото
# img = cv2.imread('Machine_vision\src\VKA_promo.png') # загружаем фото
# # img = cv2.GaussianBlur(img, (9,9), 8) # Размытие по Гауссу
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Приводим картинку к Ч/Б варианту
# img = cv2.Canny(img, 150,150) # Находим контуры изображения. Параметры : исходное изображение, пароги 
# ## Изменение обводки
# kernel = np.ones((5,5), np.uint8) # Создаём матрицу границ
# # img = cv2.dilate(img, kernel, iterations=1) # Увеличиваем размер найденных ранее границ (контуров)

# # img  = cv2.erode(img, kernel, iterations=1) # Уменьшение размера найденных ранее границ (контуров)

# cv2.imshow('photo', img) # Показываем фото
# # cv2.imshow('photo', img[0:100, 0:1500]) # Показываем часть фото (левый верхний квадрат размером высота на ширина)
# cv2.waitKey(0) # Сколько картинка будет открыта. 0 == бесконечность

# #Чтение видео
# video = cv2.VideoCapture('Machine_vision\src\Gorin_video.mp4') # Читаем видео
# while True: # Цикл показа видео "по кадрам"
#     success, frame = video.read() # Получаем статус чтения(Успешно/неуспешно) и текущий кадр
#     cv2.imshow('video', frame) # Показываем текущий кадр
    
#     if ord('q') == 0xFF & cv2.waitKey(1) : # Если нажата кнопка "q" и видео кончилось 
#         break # То закрываем окно с видео

# #Работа с веб-камерами 
# video = cv2.VideoCapture(*Номер веб-камеры*) # Читаем видео
# video.set(3, 500) # Устанавливаем ширину
# video.set(4, 300) # Устанавливаем высоту

# Изменение размеров картинки
# img = cv2.imread('Machine_vision\src\VKA_promo.png') # загружаем фото
# print(img.shape) # Выводим на экран размер картинки в виде кортежа {высота, ширина, количество слоёв}
# resized_img = cv2.resize(img, (1000, 100)) # Меняем размер фото с параметрами в виде кортежа (ширина, высота)

# cv2.imshow('photo', resized_img) # Показываем фото

# cv2.waitKey(0) # Сколько картинка будет открыта. 0 == бесконечность

# Создание собственных изобращений
# Для создание изображений используется матрица
photo= np.zeros((300, 300, 3), dtype='uint8') # Создаём матрицу, которая является "холстом" размером ширина на высоту пикселей глубиной 3
# В OpenCV используется формат BGR
# photo[:] = 255, 0, 255 # Красим ВСЁ изображение (Синий ,зелёный, красный)
# photo[10:100, 10:100] = 0, 255, 255 # Красим С ОТСТУПАМИ изображение (Синий ,зелёный, красный)
## Рисуем квадрат
cv2.rectangle(photo, (0, 0), (100, 100), (200, 200,0), thickness=3) # Рисуем квадрат. Параметры : "холст", (отступ от левого верхнего края), (размер квадрата), (цвет обводки), толщена обводки

cv2.imshow('photo', photo) # Показываем фото
cv2.waitKey(0) # Сколько картинка будет открыта. 0 == бесконечность

