import cv2
import sys
import os.path
import os, psutil

# def detect(filename, cascade_file = "Machine_vision\Models\lbpcascade_animeface.xml"):
#     if not os.path.isfile(cascade_file):
#         raise RuntimeError("%s: not found" % cascade_file)

#     cascade = cv2.CascadeClassifier(cascade_file)
#     image = cv2.imread(filename, cv2.IMREAD_COLOR)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.equalizeHist(gray)
    
#     faces = cascade.detectMultiScale(gray,
#                                      # detector options
#                                      scaleFactor = 1.1,
#                                      minNeighbors = 5,
#                                      minSize = (24, 24))
#     for (x, y, w, h) in faces:
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

#     cv2.imshow("AnimeFaceDetect", image)
#     cv2.waitKey(0)
#     cv2.imwrite("out.png", image)



# if len(sys.argv) != 2:
#     sys.stderr.write("usage: detect.py <filename>\n")
#     sys.exit(-1)
    
# detect(sys.argv[1])

# path = r'Machine_vision\Datasets\anime_faces\data\data\1.png'
zero_ram = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

min_start_ram = 9999
min_end_ram = 99999

max_start_ram = -1
max_end_ram = -1

cascade_file = "Machine_vision\Models\lbpcascade_animeface.xml"
directory = r'Machine_vision\Datasets\anime_faces\data\data'

for file in os.listdir(directory): 
    
    start_ram = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    
    if start_ram > max_start_ram : max_start_ram = start_ram
    elif start_ram < min_start_ram : min_start_ram = start_ram
    
    filename = os.path.join(directory, file)
    # checking if it is a file
    if os.path.isfile(filename):
        print(filename)
        
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                        # detector options
                                        scaleFactor = 1.1,
                                        minNeighbors = 5,
                                        minSize = (24, 24))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        end_ram = (psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
        
        if end_ram > max_end_ram : max_end_ram = end_ram
        elif end_ram < min_end_ram : min_end_ram = end_ram
        
print(zero_ram, '\n', min_start_ram, max_start_ram, '\n', min_end_ram, max_end_ram)
        
        # cv2.imshow("AnimeFaceDetect", image)
        # cv2.waitKey(0)
        # cv2.imwrite("out.png", image)


