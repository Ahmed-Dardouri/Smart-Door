'''import face_recognition 
import glob
import cv2 
import numpy as np
path = glob.glob("members/*")
a = path[0]
path[0] = path[2]
path[2] = a
cv_img = []
for img in path:
    print(img)
    n = cv2.imread(img)
    cv_img.append(n)

def findencodings(images): 
   encodelist=[] 
   for img in images :
      img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
      encod=face_recognition.face_encodings(img)[0] 
      encodelist.append(encod) 
   return encodelist
encodelistknown=findencodings(cv_img)
cap=cv2.VideoCapture(0) 
while True : 
  ret, img= cap.read()
  imgs = img
  imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB) 
  facescurframe=face_recognition.face_locations(imgs) 
  encodescurframe=face_recognition.face_encodings(imgs,facescurframe)
  for encodface,faceloc in zip(encodescurframe,facescurframe): 
      matches=face_recognition.compare_faces(encodelistknown,encodface)
      facedis=face_recognition.face_distance(encodelistknown,encodface) 
      y1,x2,y2,x1 = faceloc
      if(facedis.size>0):
        matchindex=np.argmin(facedis)
        if (matches[matchindex]):
          cv2.rectangle(imgs,(x1,y1),(x2,y2),(0,255,0),2)
        print(matchindex)
      
  cv2.imshow('cap',imgs)
  if cv2.waitKey(1) & 0xFF == ord('q'):
        break'''








import cv2
import numpy as np
import dlib
import face_recognition
import glob
import time
import threading
from multiprocessing import Process, Pipe, Event

def CaptureProcess(pipe, read_ev):
    while True:
        video = None
        def read_th():
            success = False
            while True:
                if(success): read_ev.wait()
                while video is None or not video.isOpened(): pass
                success, imageFrame = video.read()
                if(success): 
                    pipe.send(imageFrame)
                    print('send')
        r_th = threading.Thread(target=read_th)
        r_th.daemon = True
        r_th.start()
        while True:
            c = (video is None or not video.isOpened())
            if c:
                video = cv2.VideoCapture(0)
            c = (video is None or not video.isOpened())
            if c: 
                time.sleep(0.5)
                
            elif(not read_ev.is_set()):
                video.grab()
                print('grab')
                

class InferThread(threading.Thread):
    def __init__(self):
        super(InferThread, self).__init__()
        self.daemon = True
    def run(self):
        global cap_read_ev, cap_pipe, encodeListunknown
        while True:
            cap_read_ev.set()
            img = cap_pipe.recv()
            cap_read_ev.clear()
            
            imgs=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
            facescurframe=face_recognition.face_locations(imgs) 
            encodescurframe=face_recognition.face_encodings(imgs,facescurframe)
            for encodface,faceloc in zip(encodescurframe,facescurframe): 
                matches=face_recognition.compare_faces(encodelistknown,encodface)
                facedis=face_recognition.face_distance(encodelistknown,encodface) 
                y1,x2,y2,x1 = faceloc
                if(facedis.size>0):
                  matchindex=np.argmin(facedis)
                  if (matches[matchindex]):
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                  print(matchindex)

                
            cv2.imshow('cap',img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break

path = glob.glob("members/*")
a = path[0]
path[0] = path[2]
path[2] = a
cv_img = []
for img in path:
    print(img)
    n = cv2.imread(img)
    cv_img.append(n)

def findencodings(images):
   encodelist=[]
   for img in images :
      img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
      encod=face_recognition.face_encodings(img)[0] 
      encodelist.append(encod) 
   return encodelist
encodelistknown=findencodings(cv_img)


cap_pipe, cap_child_pip = Pipe()
cap_read_ev = Event()
cap_read_ev.set()

infer_th=InferThread()

cap_process=Process(target=CaptureProcess, args=(cap_child_pip, cap_read_ev))
cap_process.daemon = False
cap_process.start()

infer_th.start()
