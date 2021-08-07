# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 22:58:14 2021

@author: Mahfuz_Shazol
"""

import cv2
import time
import HandTrackingModule as htm
import autopy
import numpy as np

wCam,hCam=640,480
frameReduction=100
smoothening=5

cTime = 0
pTime = 0
preLockX,preLockY=0,0
currLockX,currLockY=0,0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)



detector=htm.handDetector(maxHand=1)

wScr,hScr=autopy.screen.size() #get device screen size

while True:
    success,img=cap.read()
    img=detector.findHands(img,draw=(False))
    lmkList,bbox=detector.findSumthPosition(img,draw=(False))
    
    if len(lmkList)!=0:
        x1,y1=lmkList[8][1:]
        x2,y2=lmkList[12][1:]
        #print(x1,y1,'------',x2,y2)
        
        fingures=detector.fingursUp()
        #print(fingures)
        cv2.rectangle(img, (frameReduction,frameReduction), (wCam-frameReduction,hCam-frameReduction), (255,0,0))
        
        if fingures[1]==1 and fingures[2]==0:
              #print('Moving')
              x3=np.interp(x1,(frameReduction,wCam-frameReduction),(0,wScr))
              y3=np.interp(y1,(frameReduction,hCam-frameReduction),(0,hScr))

              currLockX=preLockX+(x3-preLockX)/smoothening
              currLockY=preLockY+(y3-preLockY)/smoothening
              
              autopy.mouse.move(wScr-currLockX, currLockY)
              cv2.circle(img,(x1,y1), 15,(255,0,0),cv2.FILLED)
              preLockX=currLockX
              preLockY=currLockY
              
        elif fingures[1]==1 and fingures[2]==1:
              #print('selection')
              length,img,line=detector.findDistance(8,12,img,draw=False)
              print(length)
              if length<30:
                  cv2.circle(img,(line[4],line[5]), 15,(255,255,255),cv2.FILLED)
                  autopy.mouse.click()
              


    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70),cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
           
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xff==ord('c'):
               cap.release()
               cv2.destroyAllWindows()
               break;





