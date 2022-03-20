import face_recognition 
import glob
import cv2 
import numpy as np
path = glob.glob("members/*")
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
  imgs = cv2.resize(img,(0,0),None,0.25,0.25)
  imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB) 
  facescurframe=face_recognition.face_locations(imgs) 
  encodescurframe=face_recognition.face_encodings(imgs,facescurframe)
  for encodface,faceloc in zip(encodescurframe,facescurframe): 
      matches=face_recognition.compare_faces(encodelistknown,encodface)
      facedis=face_recognition.face_distance(encodelistknown,encodface) 
      if(facedis.size>0):
        
        matchindex=np.argmin(facedis)
        print(matchindex)
        '''if(matches[matchindex]) : 
            name=classname[matchindex].upper() 
            print(name)'''
      
  cv2.imshow('cap',img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
        break