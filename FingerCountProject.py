# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 23:24:32 2021

@author: Mahfuz_Shazol
"""

import cv2
import mediapipe as mp
import time
import os
import HandTrackingModule as htm

cTime = 0
pTime = 0

cap=cv2.VideoCapture(0)
wCam,hCam=640,480
cap.set(3,wCam)
cap.set(4,hCam)

folderDir='CountFiles'
myList=os.listdir(folderDir)
overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderDir}/{imPath}')
    overlayList.append(image)
print(len(overlayList))    

detector=htm.handDetector(detectionConf=0.7)

tipIds=[4,8,12,16,20]

while True:
        success, img = cap.read()

        img=detector.findHands(img)
        lmkList=detector.findPosition(img,draw=False)
        #print(lmkList)
        if len(lmkList)!=0:
            fingers=[]
            #Thumb
            if lmkList[tipIds[0]][1]>lmkList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            #4 fingers
            for id in range(1,5):    
                if lmkList[tipIds[id]][2]<lmkList[tipIds[id]-2][2]:
                   fingers.append(1) 
                else:
                   fingers.append(0)
            print(fingers)    
            totalCount=fingers.count(1)
            
            
            
            if totalCount==0:
                h,w,c=overlayList[5].shape
                img[0:h,0:w]=overlayList[5]
                cv2.rectangle(img,(0,0),(w,h), (255,0,0),2)
            else:
                h,w,c=overlayList[totalCount-1].shape
                img[0:h,0:w]=overlayList[totalCount-1]
                cv2.rectangle(img,(0,0),(w,h), (255,0,0),2)    
            cv2.putText(img, f'Total: {totalCount}', (0, 165), cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),1)          
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (400, 50), cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),3)      
        cv2.imshow("Images", img)
        cv2.waitKey(1)

        if cv2.waitKey(1) & 0xff == ord('c'):
             cap.release()
             cv2.destroyAllWindows()
             break
