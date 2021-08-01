# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 17:44:07 2021

@author: Mahfuz_Shazol
"""

import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



def releaseCameraAndColseWindow():     
           cap.release()
           cv2.destroyAllWindows()
           
           


cTime=0
pTime=0

cap=cv2.VideoCapture(0)
wCam,hCam=640,480
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector(detectionConf=0.75)
    
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minVol=volumeRange[0]
maxVol=volumeRange[1]

volBar=400
volPer=0

while True:
        try:
          success,img=cap.read()
           
          img=detector.findHands(img,draw=False)
                   
          lmkList=detector.findPosition(img,draw=False)
          
          if len(lmkList)!=0:
               #print(lmkList[4],lmkList[8])
               
               x1,y1=lmkList[4][1],lmkList[4][2]
               x2,y2=lmkList[8][1],lmkList[8][2]
               cx,cy=(x1+x2)//2,(y1+y2)//2
               
               
               cv2.circle(img, (x1,y1), 2, (0,255,0),cv2.FILLED)
               cv2.circle(img, (x2,y2), 2, (0,255,0),cv2.FILLED)
               cv2.line(img, (x1,y1), (x2,y2), (255,0,0),1)
               cv2.circle(img, (cx,cy), 2, (0,255,0),cv2.FILLED)
               
               length=math.hypot(x2-x1,y2-y1)
               #print(length)
               
               #Hand Range 50-300
               #Volume Range (-65)-0
               
               vol=np.interp(length,[50,300],[minVol,maxVol])
               volBar=np.interp(length,[50,300],[400,150])
               volPer=np.interp(length,[50,300],[0,100])
               print(vol) 
               volume.SetMasterVolumeLevel(vol, None)
                 
               if length<50:
                   cv2.circle(img, (cx,cy), 2, (255,0,0),cv2.FILLED)
               
          cv2.rectangle(img,(50,150),(85,400), (255,255,255),3)
          cv2.rectangle(img,(50,int(volBar)),(85,400),(255,255,255),cv2.FILLED)
          cv2.putText(img,f'{int(volPer)}%',(50,140),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)      
          
          cTime=time.time()
          fps=1/(cTime-pTime)
          pTime=cTime
          
          cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)      
          cv2.imshow("Images",img)
          cv2.waitKey(10)      
          if cv2.waitKey(1) & 0xff==ord('c'):
              releaseCameraAndColseWindow()
              break;      
           
        except Exception as e:
               releaseCameraAndColseWindow()             
               print(e)       
           
      
        
      
        

           