# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 14:48:46 2021

@author: Mahfuz_Shazol
"""

import cv2
import mediapipe as mp
import time


cTime=0
pTime=0
cap=cv2.VideoCapture(0)


mpDraw=mp.solutions.drawing_utils
mpFaceMesh=mp.solutions.face_mesh
faceMesh=mpFaceMesh.FaceMesh()
drawSpec=mpDraw.DrawingSpec(thickness=1,circle_radius=1)

while True:
       success,img=cap.read()
       imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
       results=faceMesh.process(imgRGB)
       
       if results.multi_face_landmarks:
           for faceLms in results.multi_face_landmarks:
                 mpDraw.draw_landmarks(img, faceLms,mpFaceMesh.FACE_CONNECTIONS,drawSpec,drawSpec)
       
                 for id,lm in enumerate(faceLms.landmark):
                     #print(lm) 
                     ih,iw,ic=img.shape
                     x,y=int(lm.x*iw),int(lm.y*ih)
                     print(id,x,y)
       cTime=time.time()
       fps=1/(cTime-pTime)
       pTime=cTime
      
      
       cv2.putText(img,f'FPS:{int(fps)}',(70,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)   
       cv2.imshow("Images",img)
       cv2.waitKey(1)
       
       if cv2.waitKey(1) & 0xff==ord('c'):
             cap.release()
             cv2.destroyAllWindows()
             break;