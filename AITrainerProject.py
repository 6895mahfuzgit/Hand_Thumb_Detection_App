# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 19:48:47 2021

@author: Mahfuz_Shazol
"""

import cv2
import mediapipe as mp
import time
import PoseModule as pm
import numpy as np

cTime=0
pTime=0
cap=cv2.VideoCapture(0)
detector=pm.poseDetector()    

count=0
dirr=0

while True:
      success,img=cap.read()
      img=cv2.resize(img, (640,480))
      
      img=detector.findPose(img,drow=False)    
      
      lmkList=detector.getPosition(img,drow=False)
      
      #print(lmkList)
      if len(lmkList)!=0:
          #Right Arm
          angle=detector.findAngle(img, 12, 14, 16)
          per=np.interp(angle,(210,310),(0,100))
          #print('Angle:',angle,'Count:',per)
          #Check For The Dumble CURLs
          if per==100:
              if dirr==0:
                  count+=0.5
                  dirr=1
          if per==0:
              if dirr==1:
                  count+=0.5
                  dirr=0
                  
          #print(count)
          cv2.circle(img, (65,80), 50, (255,0,0),cv2.FILLED)
          #cv2.circle(img,f'{str(int(count))}',(50,100),15,(255,0,0),3)            
          cv2.putText(img,f'{str(int(count))}',(50,100),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)            
            
          #Left Arm
          #detector.findAngle(img, 11, 13, 15)
          
          #Right Leg
          #detector.findAngle(img, 23, 25, 27)
          
          #Left Leg
          #detector.findAngle(img, 24, 26, 28)
      
      cTime=time.time()
      fps=1/(cTime-pTime)
      pTime=cTime
      
      
      cv2.putText(img,f'FPS:{int(fps)}',(400,50),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)      
      cv2.imshow("Images",img)
      cv2.waitKey(1)
      
      if cv2.waitKey(1) & 0xff==ord('c'):
             cap.release()
             cv2.destroyAllWindows()
             break;
