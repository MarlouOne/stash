import cv2
import numpy as np
from random import randint
from PIL import Image

img1 = cv2.imread(r'C:\Users\major\Documents\GitHub\stash\augmentation\samples\argus\back\1.png')

# height, width = 3000, 3000
# img1 = np.ones( ( height, width, 3) , dtype='uint8') # zeros
# img2 = cv2.imread(r'C:\Users\major\Documents\GitHub\stash\augmentation\samples\argus\image\gear\1.png')
img2 = cv2.imread(r'augmentation\\samples\\argus\\image\\i_box\\1.png')


x = randint(0, img1.shape[1]-img2.shape[1])
y = randint(0, img1.shape[0]-img2.shape[0])


# Разместите логотип в верхнем левом углу, чтобы нас интересовала только эта область
rows, cols = img2.shape[:2]
roi = img1[:rows, :cols]

# cv2.imshow('roi',roi)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Создать маску
img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)

# cv2.imshow('mask',mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

mask_inv = cv2.bitwise_not(mask)

# Сохраните фон, кроме логотипа
img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

# background = Image.fromarray(img1_bg)
# overlay    = Image.fromarray(img2)

# background.paste(overlay.resize((overlay.width // 5, overlay.height // 5)), (200,300))
# background.show()

dst = cv2.add(img1_bg, img2)  # Выполнить фьюжн

# cv2.imshow('dst',dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img1[x:rows+x, y:cols+y] = dst  # Ставим на исходное изображение после слияния



cv2.imshow('res',cv2.resize(img1, (1024, 1024)))
cv2.waitKey(0)
cv2.destroyAllWindows()