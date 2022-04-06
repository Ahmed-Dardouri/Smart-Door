import face_recognition 
import glob
import cv2 
import numpy as np
path = glob.glob("members/*")


import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
gpio.setup(10,gpio.OUT)


    

cv_img = []
for img in path:
    print(img)
    n = cv2.imread(img)
    cv_img.append(n)
def find_face(imgs):
    ok = False
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB) 
    imgs=cv2.resize(imgs,imgs.shape // 2)
    facescurframe=face_recognition.face_locations(imgs) 
    encodescurframe=face_recognition.face_encodings(imgs,facescurframe)
    for encodface,faceloc in zip(encodescurframe,facescurframe): 
        matches=face_recognition.compare_faces(encodelistknown,encodface)
        facedis=face_recognition.face_distance(encodelistknown,encodface) 
        y1,x2,y2,x1 = faceloc
        if(facedis.size>0):
            matchindex=np.argmin(facedis)
            if (matches[matchindex]):
                ok = True
    return ok

def findencodings(images): 
   encodelist=[] 
   for img in images :
      img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
      encod=face_recognition.face_encodings(img)[0] 
      encodelist.append(encod) 
   return encodelist

encodelistknown=findencodings(cv_img)


cap=cv2.VideoCapture(0)
for i in range(30):
    if(i % 3 == 0):
        ret, img= cap.read()
        f = find_face(img)
        print(f)
        if (f):
            open_door()
            
    else:
        cap.grab()

    
def open_door():
    gpio.output(10,1)
    gpio.output(11,0)
    time.sleep(1)
    gpio.output(10,0)
    gpio.output(11,0)
    time.sleep(3)
    gpio.output(10,0)
    gpio.output(11,1)
    

