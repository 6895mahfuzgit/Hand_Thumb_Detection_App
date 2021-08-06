# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:11:20 2021

@author: Mahfuz_Shazol
"""

import cv2
import mediapipe as mp
import time
import os
import HandTrackingModule as htm
import numpy as np

################################
brushThickness=15
eRaseThickness=30
################################



folderPath="PaintHeader"

myList=os.listdir(folderPath)
overlayFiles=[]

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayFiles.append(image)
header=overlayFiles[0]
drawColor=(255,0,255)

cTime=0
pTime=0
cap=cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector=htm.handDetector(detectionConf=.85)

px,py=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)


while True:
         success,img=cap.read()    
         
         img=cv2.flip(img,1) 
         
         img=detector.findHands(img,draw=(False))
         lmkList=detector.findPosition(img,draw=(True))
         
         if len(lmkList)!=0:
             x1,y1=lmkList[8][1:]
             x2,y2=lmkList[12][1:]
         
             fingurs=detector.fingursUp()
             #print(fingurs)
             if fingurs[1] and fingurs[2]:
                   px,py=0,0 
                   print('Selection Mode')
                   if y2<125:
                       if 250<x1<450:
                           header=overlayFiles[0]
                           drawColor=(255,0,255)
                       elif 550<x1<750:
                           header=overlayFiles[1]
                           drawColor=(255,0,0)
                       elif 800<x1<950:
                           header=overlayFiles[2]
                           drawColor=(0,255,0)
                       elif 1050<x1<1200:
                           header=overlayFiles[3]    
                           drawColor=(255,0,0)
                           drawColor=(0,0,0)
                   cv2.rectangle(img,(x1,y1-15),(x2,y2+15),drawColor,cv2.FILLED)
                           
             if fingurs[1] and  fingurs[2]==False:
                   cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
                   if px==0 and py==0:
                       px,py=x1,y1
                 
                       
                   if drawColor==(0,0,0):
                       cv2.line(img,(px,py),(x1,y1),drawColor,eRaseThickness)
                       cv2.line(imgCanvas,(px,py),(x1,y1),drawColor,eRaseThickness)    
                   else:    
                       cv2.line(img,(px,py),(x1,y1),drawColor,brushThickness)
                       cv2.line(imgCanvas,(px,py),(x1,y1),drawColor,brushThickness)
                       print('Drow Mode')
                   
                   px,py=x1,y1
         
            
         img[0:125,0:1280]=header
         
         
         cTime=time.time()
         fps=1/(cTime-pTime)
         pTime=cTime
         
         cv2.putText(img,f'FPS: {str(int(fps))}',(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
         
         imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
         _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
         imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
         img=cv2.bitwise_and(img,imgInv)
         img=cv2.bitwise_or(img,imgCanvas)
         
         #img=cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
         cv2.imshow("Images",img)
         #cv2.imshow("Canvas Images",imgCanvas)
         cv2.waitKey(1)
           
         if cv2.waitKey(1) & 0xff==ord('c'):
              cap.release()
              cv2.destroyAllWindows()
              break;
