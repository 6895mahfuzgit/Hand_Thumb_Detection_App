# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 00:27:14 2021

@author: Mahfuz_Shazol
"""
import cv2
import mediapipe as mp
import time
import PoseModule as pm


cTime=0
pTime=0

#cap=cv2.VideoCapture('2.mp4')
cap=cv2.VideoCapture(0)
detector=pm.poseDetector()
    
while True :
        try:
            success, img = cap.read()
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
        
            img = detector.findPose(img, drow=False)
            lmkList = detector.getPosition(img,drow=False)
            #print(lmkList)
            cv2.circle(img, (lmkList[14][1],lmkList[14][2]), 15,(0,0,255), cv2.FILLED)
            cv2.putText(img, str(int(fps)), (70, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            
            cv2.imshow("Images", img)
            cv2.waitKey(1)
        
            if cv2.waitKey(1) & 0xff == ord('c'):
                cap.release()
                cv2.destroyAllWindows()
                break
            
        except Exception as e:
                cap.release()
                cv2.destroyAllWindows()
                break
            
