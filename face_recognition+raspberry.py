import face_recognition 
import glob
import cv2 
import numpy as np

path = glob.glob("members/*")


import RPi.GPIO as gpio
import time
def open_door():
    gpio.output(10,1)
    gpio.output(11,0)
    time.sleep(1)
    gpio.output(10,0)
    gpio.output(11,0)
    time.sleep(3)
    gpio.output(10,0)
    gpio.output(11,1)
    
gpio.setmode(gpio.BOARD)
gpio.setup(10,gpio.OUT)
gpio.setup(11,gpio.OUT)
gpio.setup(13,gpio.OUT)#green led
gpio.setup(15, gpio.OUT)# red led


    

cv_img = []
for img in path:
    print(img)
    n = cv2.imread(img)
    cv_img.append(n)
def find_face(imgs):
    ok = False
    imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB) 
    '''imgs=cv2.resize(imgs,imgs.shape // 2)'''
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

print('start')
gpio.setwarnings(False) 
gpio.setmode(gpio.BOARD) 
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_DOWN)
cap=cv2.VideoCapture(0)
while True:
   
    if gpio.input(12) == gpio.HIGH:
        print("Button was pushed!")
        gpio.output(13,1)
        
        gpio.output(13,0)
        f = False
        i = 0
        img = 0
        while (i<30 and not(f)) :
            i+=1
            if(i % 3 == 0):
                ret, img= cap.read()
                f = find_face(img)
                print(f)
                if (f):
                    gpio.output(15, 0)
                    gpio.output(13, 1)
                    open_door()
                    gpio.output(13, 0)
                    
                    break
                else:
                    gpio.output(15, 1)
            
            else:
                cap.grab()
        gpio.output(15, 0)
        gpio.output(13, 0)
    else:
        cap.grab()




        
